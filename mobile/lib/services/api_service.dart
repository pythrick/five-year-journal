import 'dart:convert';
import 'dart:io';

import 'package:dio/dio.dart';
import 'package:five_year_journal/models.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

class ApiService {
  Dio api = Dio(BaseOptions(
      baseUrl: "https://five-year-journal-api.herokuapp.com/v1",
      headers: {
        "Content-Type": "application/json",
      }));

  ApiService() {
    api.interceptors.add(InterceptorsWrapper(onRequest:
        (RequestOptions options, RequestInterceptorHandler handler) async {
      if (!options.headers.containsKey("requiresToken")) {
        return handler.next(options);
      }
      options.headers.remove("requiresAuth");

      SharedPreferences preferences = await SharedPreferences.getInstance();
      String accessToken = preferences.getString("accessToken") ?? "";
      String refreshToken = preferences.getString("refreshToken") ?? "";

      if (accessToken.isEmpty || refreshToken.isEmpty) {
        DioError _err = DioError(
            requestOptions: options, error: "Credentials not in storage.");
        return handler.reject(_err);
      }

      bool refreshTokenHasExpired = JwtDecoder.isExpired(refreshToken);
      if (refreshTokenHasExpired) {
        preferences.remove("accessToken");
        preferences.remove("refreshToken");
        DioError _err =
            DioError(requestOptions: options, error: "Credentials expired.");
        return handler.reject(_err);
      }

      bool accessTokenHasExpired = JwtDecoder.isExpired(accessToken);
      if (accessTokenHasExpired) {
        Token? token = await this.refreshToken();
        accessToken = token!.accessToken;
      }

      options.headers["Authorization"] = "Bearer $accessToken";
      return handler.next(options);
    }, onResponse:
        (Response response, ResponseInterceptorHandler handler) async {
      return handler.next(response);
    }, onError: (DioError error, handler) async {
      return handler.next(error);
    }));
  }

  Future<List<JournalLog>?> getJournalLogs(int day, int month) async {
    Response<List<JournalLog>> res = await api.get("/journal-logs/",
        queryParameters: {
          "day": day,
          "month": month,
          "limit": 100,
          "offset": 0,
        },
        options: Options(headers: {"requiresAuth": true}));
    if (res.statusCode != HttpStatus.ok) {
      throw "Failed to load journal logs list";
    }
    return res.data;
  }

  Future<JournalLog?> createJournalLog(JournalLog journalLog) async {
    final Response<JournalLog> res = await api.post("/journal-logs/",
        data: {'content': journalLog.content},
        options: Options(headers: {"requiresAuth": true}));
    if (res.statusCode != HttpStatus.created) {
      throw "Failed to create journal log";
    }
    return res.data;
  }

  Future<Token?> getToken(Account account) async {
    final Response<Token> res = await api.post(
      "/auth/token",
      data: {
        'email': account.email,
        "password": account.password,
      },
    );
    if (res.statusCode != HttpStatus.ok) {
      throw "Authentication failed";
    }
    SharedPreferences preferences = await SharedPreferences.getInstance();
    await preferences.setString("accessToken", res.data!.accessToken);
    await preferences.setString("refreshToken", res.data!.refreshToken);
    return res.data;
  }

  Future<Token?> refreshToken() async {
    SharedPreferences preferences = await SharedPreferences.getInstance();
    String? refreshToken = preferences.getString("refreshToken");

    final Response<Token> res = await api.post(
      "/auth/refresh",
      data: {
        'refreshToken': refreshToken,
      },
    );
    if (res.statusCode != HttpStatus.ok) {
      throw "Authentication failed";
    }
    await preferences.setString("accessToken", res.data!.accessToken);
    await preferences.setString("refreshToken", res.data!.refreshToken);
    return res.data;
  }

  Future<Account?> createAccount(Account account) async {
    final Response<Account> res = await api.post(
      "/accounts/",
      data: {
        "name": account.name,
        'email': account.email,
        "password": account.password,
      },
    );
    if (res.statusCode != HttpStatus.created) {
      throw "Failed to create account.";
    }
    return res.data;
  }
}
