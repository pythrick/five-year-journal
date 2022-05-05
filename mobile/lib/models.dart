import 'package:uuid/uuid.dart';

class JournalLog {
  final Uuid? id;
  final String content;
  final DateTime? createdAt;

  const JournalLog({
    this.id,
    required this.content,
    this.createdAt,
  });

  // factory JournalLog.fromJson(Map<String, dynamic> json){
  //   return JournalLog(
  //     id: json["id"] as Uuid,
  //     content: json["content"] as String,
  //     createdAt: json["createdAt"] as DateTime,
  //   );
  // }

  @override
  String toString() {
    return 'JournalLog(id: $id, content: $content, createdAt: $createdAt)';
  }
}


class Account {
  final Uuid? id;
  final String? name;
  final String email;
  final String? password;

  const Account({
    this.id,
    this.name,
    required this.email,
    this.password,
  });

  // factory Account.fromJson(Map<String, dynamic> json) {
  //   return Account(
  //       id: json["id"] as Uuid,
  //       name: json["name"] as String,
  //       email: json["email"] as String,
  //   );
  // }

  @override
  String toString() {
    return "Account(id: $id, name: $name, email: $email, password: *******)";
  }
}

class Token {
  final String accessToken;
  final String refreshToken;

  const Token({
    required this.accessToken,
    required this.refreshToken,
  });

  // factory Credentials.fromJson(Map<String, dynamic> json) {
  //   return Credentials(
  //     accessToken: json["accessToken"],
  //     refreshToken: json["refreshToken"],
  //   );
  // }
}
