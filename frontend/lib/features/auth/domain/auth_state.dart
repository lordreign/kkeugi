import '../data/auth_api.dart';

enum AuthStatus { unknown, unauthenticated, authenticated }

class AuthState {
  const AuthState({required this.status, this.user});

  const AuthState.unknown() : status = AuthStatus.unknown, user = null;
  const AuthState.unauthenticated()
      : status = AuthStatus.unauthenticated,
        user = null;
  const AuthState.authenticated(this.user) : status = AuthStatus.authenticated;

  final AuthStatus status;
  final UserResponse? user;

  bool get isAuthenticated => status == AuthStatus.authenticated;
}
