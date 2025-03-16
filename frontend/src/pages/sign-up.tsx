import { useState } from 'react';
import { auth, googleProvider } from '../config/firebase';
import { createUserWithEmailAndPassword, signInWithPopup } from 'firebase/auth';

const SignUp = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const signInWithGoogle = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      alert('Signed in successfully with Google');
    } catch (error) {
      console.error('Error signing in with Google', error);
    }
  };

  const handleCreateUser = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      alert('User created successfully');
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <h2>Register your Account</h2>
      <form onSubmit={handleCreateUser}>
        <div>
          <label>Name</label>
          <input
            type='text'
            id='name'
            name='name'
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor='email'>Email</label>
          <input
            type='email'
            id='email'
            name='email'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor='password'>Password</label>
          <input
            type='password'
            id='password'
            name='password'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor='confirm_password'>
            Confirm Password
          </label>
          <input
            type='password'
            id='confirm_password'
            name='confirm_password'
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        <div>
          <div>
            <input
              type='checkbox'
              id='terms'
              name='terms'
              className='mr-2'
            />
            <label htmlFor='terms'>
              I agree to the{' '}
              <a href='#'>
                Terms and Conditions
              </a>
            </label>
          </div>
        </div>

        <button type='submit'>Register</button>
      </form>
      
      <button onClick={signInWithGoogle}>Sign in with Google</button>
    </div>
  );
};

export default SignUp;