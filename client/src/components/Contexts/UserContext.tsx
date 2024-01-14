import React, { useState, useEffect, createContext, ReactNode, FC } from 'react';

// Define a type for the user state
type UserState = {
  uid: string;
} | null;

// Define a type for the context
type UserContextType = {
  user: UserState;
  setUser: React.Dispatch<React.SetStateAction<UserState>>;
};

// Create the context with a default value
const UserContext = createContext<UserContextType>({
  user: null,
  setUser: () => {}, // Placeholder function
});

// Define a type for the props of UserProvider
type UserProviderProps = {
  children: ReactNode;
};

// UserProvider component with typed props
export const UserProvider: FC<UserProviderProps> = ({ children }) => {
  // Initialize user state from localStorage
  const initialUser: UserState = JSON.parse(localStorage.getItem('user')!) || null;

  const [user, setUser] = useState<UserState>(initialUser);

  // Use useEffect to update localStorage whenever user state changes
  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  }, [user]);

  return <UserContext.Provider value={{ user, setUser }}>{children}</UserContext.Provider>;
};

export default UserContext;