import React, { useState, useEffect, ReactNode } from 'react';
import UserContext from './UserContext';

// Define the type for user data
interface User {
  // Add properties for your user data here
  uid: string;
  name: string;
  email: string;
}

// Define the type for the component props
interface UserProviderProps {
  children: ReactNode;
}

const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  // Initialize user state from localStorage
  const initialUser = JSON.parse(localStorage.getItem('user') || 'null') as User | null;

  const [user, setUser] = useState<User | null>(initialUser);

  // Use useEffect to update localStorage whenever user state changes
  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  }, [user]);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserProvider;
