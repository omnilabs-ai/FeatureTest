import { auth } from '../config/firebase'; // Adjust the path based on your file structure
import { signOut } from 'firebase/auth';

const SignOut = () => {
  const handleSignOut = async () => {
    try {
      await signOut(auth);
    alert('User signed out successfully');
  } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <div>
      <button onClick={handleSignOut}>Sign Out</button>
    </div>
  );
};

export default SignOut;
