from passlib.context import CryptContext

# Create a CryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def bcrypt(password: str):
        """
        Hash a password using bcrypt
        
        Args:
            password (str): Plain text password to be hashed
        
        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify(hashed_password: str, plain_password: str):
        """
        Verify a password against its hash
        
        Args:
            hashed_password (str): Previously hashed password
            plain_password (str): Plain text password to verify
        
        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)