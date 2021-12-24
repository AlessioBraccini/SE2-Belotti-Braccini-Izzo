import { createRouter, createWebHistory } from 'vue-router'
import About from "../views/About.vue"
import NotFound from "@/views/NotFound";
import SignUpForm from "@/components/SignUpForm";
import LoginPage from "@/views/LoginPage";

const routes = [
    {
        path: '/',
        name: 'Login',
        component: LoginPage
    },
    {
        path: '/about',
        name: 'About',
        // component: () => import('../views/About.vue')
        component: About
    },
    {
        path: '/signUp',
        name: 'SignUp',
        // component: () => import('../views/About.vue')
        component: SignUpForm
    },
    // Catch 404
    {
        path: '/:catchAll(.*)',
        name: 'NotFound',
        component: NotFound
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router