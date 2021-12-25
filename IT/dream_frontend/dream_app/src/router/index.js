import { createRouter, createWebHistory } from 'vue-router'
import About from "../views/About.vue"
import NotFound from "@/views/NotFound";
import SignUpForm from "@/components/SignUpForm";
import LoginPage from "@/views/LoginPage";
import PolicyMakerHomepage from "@/views/PolicyMakerHomepage";
import AgronomistHomepage from "@/views/AgronomistHomepage";

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
    {
        path: '/agronomistHome',
        name: 'AgroHome',
        // component: () => import('../views/About.vue')
        component: AgronomistHomepage
    },
    {
        path: '/policymakerHome',
        name: 'PMHome',
        // component: () => import('../views/About.vue')
        component: PolicyMakerHomepage
    },
    // Catch 404
    {
        path: '/:catchAll(.*)',
        name: 'NotFound',
        component: NotFound
    }
]

// To cycle between farmers specification see this video for the links with the ':'
// https://www.youtube.com/watch?v=juocv4AtrHo&list=PL4cUxeGkcC9hYYGbV60Vq3IXYNfDk8At1&index=9

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router