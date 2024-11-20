export default defineNuxtRouteMiddleware((to, from) => {
    const isAuthenticated = useCookie('isLoggedIn').value;
    const isAuthPage = to.path === '/login' || to.path === '/register';

    if (isAuthPage && isAuthenticated) {
        return navigateTo('/')
    }

    if (!isAuthPage && !isAuthenticated) {
        return navigateTo('/login')
    }
});
