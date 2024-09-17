import { writable } from 'svelte/store';

// Store for managing the JWT token
export const token = writable(null);

// Store for managing user information
export const user = writable({
  isAuthenticated: false,
  username: null,
  role: null
});
