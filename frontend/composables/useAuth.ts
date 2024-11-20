import {jwtDecode} from "jwt-decode"

export default () => {
    const useAuthToken = () => useState('auth_token')
    const useAuthUser = () => useState('auth_user')
    const useAuthLoading = () => useState('auth_loading', () => true)

    const setToken = (newToken) => {
        const authToken = useAuthToken()
        authToken.value = newToken
    }

    const setUser = (newUser) => {
        const authUser = useAuthUser()
        authUser.value = newUser
    }

    const setIsAuthLoading = (value) => {
        const authLoading = useAuthLoading()
        authLoading.value = value
    }

    const login = ({ email, password }) => {
        return new Promise(async (resolve, reject) => {
            try {
                const data = await useFetchApi('https://puso-be.vercel.app/auth/login', {
                    method: 'POST',
                    body: {
                        email,
                        password
                    }
                })

                setToken(data.access_token)
                setUser(data.user)
                useCookie('isLoggedIn').value = true
                resolve(true)
            } catch (error) {
                reject(error)
            }
        })
    }

    const refreshToken = () => {
        return new Promise(async (resolve, reject) => {
            try {
                const data = await useFetchApi('https://puso-be.vercel.app/auth/refresh', {
                    method: 'POST',
                })
                setToken(data.access_token)
                resolve(true)
            } catch (error) {
                await logout();
                reject(error)
            }
        })
    }

    const getUser = () => {
        return new Promise(async (resolve, reject) => {
            try {
                const data = await useFetchApi('https://puso-be.vercel.app/auth/user')

                setUser(data.data)
                resolve(true)
            } catch (error) {
                await logout()
                reject(error)
            }
        })
    }

    const reRefreshAccessToken = () => {
        const authToken = useAuthToken()

        if (!authToken.value) {
            return
        }

        const jwt = jwtDecode(authToken.value)

        const newRefreshTime = jwt.exp - 60000

        setTimeout(async () => {
            await refreshToken()
            reRefreshAccessToken()
        }, newRefreshTime);
    }

    const initAuth = () => {
        return new Promise(async (resolve, reject) => {
            setIsAuthLoading(true)
            try {
                await refreshToken()
                await getUser()

                reRefreshAccessToken()

                resolve(true)
            } catch (error) {
                console.log(error)
                reject(error)
            } finally {
                setIsAuthLoading(false)
            }
        })
    }

    const logout = () => {
        return new Promise(async (resolve, reject) => {
            try {
                await useFetchApi('https://puso-be.vercel.app/auth/logout', {
                    method: 'POST'
                })

                setToken(null)
                setUser(null)
                useCookie('isLoggedIn').value = ''
                resolve(true)
            } catch (error) {
                reject(error)
            }
        })
    }

    return {
        login,
        useAuthUser,
        useAuthToken,
        initAuth,
        useAuthLoading,
        logout
    }
}