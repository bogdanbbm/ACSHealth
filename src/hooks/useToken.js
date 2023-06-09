import { useState } from 'react';

/** Custom hook to manage the authentication token. Wraps around the useState hook
 * and uses sessionStorage to store the token.
 *
 * This function returns an ***object***, not an array so when calling it you
 * need to use the curly braces to destructure the object.
 * ```
 * const {token, setToken} = useToken();
 * ```
 * @return {Object} the token and a function to set the token
 */
function useToken() {
  const getToken = () => {
    const tokenString = sessionStorage.getItem('token');
    console.log(tokenString)
    return tokenString;
  };

  const [token, setToken] = useState(getToken());

  const saveToken = userToken => {
    if (userToken === null) {
      sessionStorage.removeItem('token');
      setToken(null);

      return;
    }

    sessionStorage.setItem('token', userToken);
    setToken(userToken);
  };

  return {
    setToken: saveToken,
    token
  };
}

export default useToken;
