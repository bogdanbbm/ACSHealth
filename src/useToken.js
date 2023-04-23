import { useState } from 'react';

/** Custom hook to manage the token. Wraps around the useState hook
 * and uses sessionStorage to store the token.
 *
 * ! This function returns an object, not an array so when calling it you
 * need to use the curly braces to destructure the object.
 * ```
 * const {token, setToken} = useToken();
 * ```
 * @return {Object} the token and a function to set the token
 */
function useToken() {
  const getToken = () => {
    const tokenString = sessionStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    return userToken?.token;
  };

  const [token, setToken] = useState(getToken());

  const saveToken = userToken => {
    sessionStorage.setItem('token', JSON.stringify(userToken));
    setToken(userToken.token);
  };

  return {
    setToken: saveToken,
    token
  };
}

export default useToken;
