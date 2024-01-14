import { createContext, Dispatch, SetStateAction } from "react";

// Define an interface for the context value
interface UserContextType {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  user: any; // Replace 'any' with a more specific type for your user, if available
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  setUser: Dispatch<SetStateAction<any>>; // Replace 'any' with the specific type for your user
}

// Provide a default value for the context
const defaultValue: UserContextType = {
  user: null,
  setUser: () => {},
};

// Create the context with the default value
const UserContext = createContext<UserContextType>(defaultValue);

export default UserContext;
