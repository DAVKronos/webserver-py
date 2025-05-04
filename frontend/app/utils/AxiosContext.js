import React, { createContext, useState, useEffect } from 'react'
import { useAuth } from './AuthContext';
import { axiosInstance } from './rest-helper'

const AxiosContext = createContext();

export const AxiosProvider = ({ children }) => {
    const { token } = useAuth();
    
    useEffect(() => {
        const interceptor = axiosInstance.interceptors.request.use(
            (config) => {
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                } else {
                    delete config.headers.Authorization;
                }
                return config;
            },
            (error)=> Promise.reject(error)
        );

        return () => {
            axiosInstance.interceptors.request.eject(interceptor);
        };
    }, [token])


    return (
    <AxiosContext.Provider value={{  }}>
      { children }
    </AxiosContext.Provider>
    )
}

export const useAxios = () => useContext(AxiosContext);


