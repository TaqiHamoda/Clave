import * as React from "react";
import {
  useLocation,
  Navigate,
} from "react-router-dom";

import { User } from "../models/User";
import { AuthService } from "../services/AuthService";
import { ENV } from "../services/Environment";

interface UserFunction{
  (user: User | null): void;
}

interface AuthContextType {
  user: User | null;
  loaded: boolean;
  signin: (user: User, callback: UserFunction) => void;
  signedin: (callback: UserFunction) => void;
  signout: (callback: VoidFunction) => void;
}

const AuthContext = React.createContext<AuthContextType>(null!);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = React.useState<User | null>(null);

  const [loaded, setLoaded] = React.useState<boolean>(false);

  const signin = (req_user: User, callback: UserFunction) => {
    if(user != null){
      setLoaded(true);
      callback(user);
      return;
    }
    
    setLoaded(false);

    AuthService.login(req_user).then(result => {
      setUser(result);
      setLoaded(true);
      callback(result);
    });
  };

  const signedin = (callback: UserFunction) => {
    if(user != null){
      setLoaded(true);
      callback(user);

      // If the server signed out, reload the page
      AuthService.getLoggedInUser().then(result => {
        if (result == null) { window.location.reload(); }
      });

      return;
    }

    setLoaded(false);

    AuthService.getLoggedInUser().then(result => {
      setUser(result);
      setLoaded(true);
      callback(result);
    });
  };

  const signout = (callback: VoidFunction) => {
    if(user == null){
      setLoaded(true);
      callback();
      return;
    }

    setLoaded(false);

    AuthService.logout().then(() => {
      setUser(null);
      setLoaded(true);
      callback();
    });
  };

  let value = { user, loaded, signin, signedin, signout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return React.useContext(AuthContext);
}

export function RequireAuth({ children }: { children: JSX.Element }) {
  let auth = useAuth();
  let location = useLocation();

  React.useEffect(() => {
    auth.signedin(() => {});
  }, []);


  if (!auth.user) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return (<>{auth.loaded && <Navigate to={ENV.LOGIN_PATH} state={{ from: location }} replace />}</>);
  }

  return children;
}