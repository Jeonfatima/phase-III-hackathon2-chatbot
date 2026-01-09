declare module 'better-auth/client' {
  export function createAuthClient(config: any): any;
}

declare module 'better-auth/client' {
  interface AuthClient {
    useSession: any;
    signIn: any;
    signOut: any;
    signUp: any;
  }
  export function createAuthClient(config: any): AuthClient;
}
