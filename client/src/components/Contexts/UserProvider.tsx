import React, { useState, useEffect, ReactNode } from "react";
import UserContext from "./userContext";

interface UserProviderProps {
  children: ReactNode;
}

const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  // Initialize user state from localStorage
  const initialUser: User | null = JSON.parse(localStorage.getItem("user")) || null;

  const [user, setUser] = useState<User | null>(initialUser);

  // Use useEffect to update localStorage whenever user state changes
  useEffect(() => {
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserProvider;

interface User {
  // Define the properties of your user object
  // For example:
  id: string;
  // ... other properties
}
