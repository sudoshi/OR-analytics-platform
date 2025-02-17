import { useAuthLogin, useAuthRegister } from "@features/auth";
import React, {
  type ReactNode,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { createCustomContext } from "utils";

import {
  type IAuthenticationContext,
  type IAuthenticationStore,
} from "./authentication.interface";
import { DOMINO_LOGOUT } from "./authentication.logout";

export const [AuthenticationContext, useAuthentication] =
  createCustomContext<IAuthenticationContext>("Authentication Context");

export const AuthenticationProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const navigate = useNavigate();
  const [authLoading, setAuthLoading] = useState(false);
  const [store, setStore] = useState<IAuthenticationStore>({
    token: localStorage.getItem("auth_token"),
    userId: localStorage.getItem("userId"),
  });

  const { mutateAsync: postAuthLogin } = useAuthLogin();
  const { mutateAsync: postAuthRegister } = useAuthRegister();

  const isLogged = useRef(!!store.token);

  const login = useCallback(
    (token: string, userId: string, tokenExpiresIn: number, redirect = "") => {
      isLogged.current = true;
      setStore((store) => ({
        ...store,
        token,
        userId,
        tokenExpiresIn,
      }));
      const currentDate = new Date();
      const tokenExpirationDate = new Date(
        currentDate.getTime() + tokenExpiresIn * 1000,
      );
      localStorage.setItem("auth_token", token);
      localStorage.setItem("userId", userId);
      localStorage.setItem(
        "tokenExpiresAtTimestamp",
        tokenExpirationDate.getTime().toString(),
      );
      navigate(redirect);
    },
    [navigate],
  );

  const logout = useCallback(() => {
    localStorage.clear();
    isLogged.current = false;
    setStore((store) => ({
      ...store,
      token: null,
    }));
    navigate("/sign-in");
  }, [navigate]);

  const authenticate = useCallback(
    async (email: string, password: string) => {
      setAuthLoading(true);
      await postAuthLogin({ email, password })
        .then((res) => {
          login(
            res.access_token,
            res.user_id,
            res.token_expires_in,
            "/workspaces",
          );
        })
        .finally(() => {
          setAuthLoading(false);
        });
    },
    [login],
  );

  const register = useCallback(
    async (email: string, password: string) => {
      setAuthLoading(true);
      postAuthRegister({ email, password })
        .then((res) => {
          if (res?.user_id) {
            toast.success("E-mail and password registered successfully!");
            void authenticate(email, password);
          }
        })
        .catch((err) => {
          console.error(err?.response);
        })
        .finally(() => {
          setAuthLoading(false);
        });
    },
    [authenticate],
  );

  const tokenExpired = useCallback(() => {
    const tokenTimestamp = localStorage.getItem("tokenExpiresAtTimestamp");
    if (tokenTimestamp) {
      const expireDate = Number(tokenTimestamp);
      const currentDate = new Date().getTime();
      return expireDate <= currentDate;
    }
    return true;
  }, []);

  /**
   * Listen to "logout" event and handles it (ie. unauthorized request)
   */
  useEffect(() => {
    window.addEventListener(DOMINO_LOGOUT, () => {
      logout();
    });
    return () => {
      window.removeEventListener(DOMINO_LOGOUT, () => {
        logout();
      });
    };
  }, [logout]);

  useEffect(() => {
    const expired = tokenExpired();
    if (expired && isLogged.current) {
      logout();
    }
  }, [tokenExpired, isLogged]);

  const value = useMemo((): IAuthenticationContext => {
    return {
      store,
      isLogged: isLogged.current,
      authLoading,
      logout,
      authenticate,
      register,
    };
  }, [store, logout, authenticate, register, authLoading]);

  return (
    <AuthenticationContext.Provider value={value}>
      {children}
    </AuthenticationContext.Provider>
  );
};
