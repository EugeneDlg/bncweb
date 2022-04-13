from passlib.context import CryptContext
def check_password(password, hashed):
    context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )
    try:
        r = context.verify(password, hashed)
    except:
        raise
    if not r:
        raise IncorrectPasswordException


def authenticate_user(login, password_entered):
    login = login.strip().lower()
    try:
        # Game.validate_user(login, op="other")
        user_data = Game.get_user_by_login(login)
        # admin_data = Game.get_user_by_login(Game.admin_user)
    except Exception:
        raise
    if not user_data:
        raise BnCException("User not found!")
    # match = re.search(r"password=\'(.*)\'", str(r0))
    password_hashed = user_data.password
    try:
        Game.check_password(password_entered, password_hashed)
    except Exception:
        return
    return True

    def get_user_by_login(login):
        try:
            session = Game.get_db_session(Game.default_db_user, Game.default_db_password)
            r0 = session.query(BnCUsers).filter_by(login=login).first()
            session.close()
        except Exception:
            try:
                session.rollback()
            except:
                pass
            raise
        return r0



