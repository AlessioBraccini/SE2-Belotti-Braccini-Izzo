import { createRouter, createWebHistory } from 'vue-router'
import About from "../views/About.vue"
import NotFound from "@/views/NotFound";
import SignUpForm from "@/components/SignUpForm";
import LoginPage from "@/views/LoginPage";
import PolicyMakerHomepage from "@/views/PolicyMaker/PolicyMakerHomepage";
import AgronomistHomepage from "@/views/Agronomist/AgronomistHomepage";
import HelpRequests from "@/views/Agronomist/HelpRequests";
import DailyPlan from "@/views/Agronomist/DailyPlan";
import WriteReport from "@/views/Agronomist/WriteReport";
import FarmerHome from "@/views/Farmer/FarmerHome";
import RankingView from "@/views/RankingView";

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
        component: SignUpForm
    },
    {
        path: '/agronomistHome',
        name: 'AgroHome',
        component: AgronomistHomepage
    },
    {
        path: '/policymakerHome',
        name: 'PMHome',
        component: PolicyMakerHomepage
    },
    {
        path: '/farmerHome',
        name: 'FarmerHome',
        component: FarmerHome
    },
    {
        path: '/agronomistHome/helpRequests',
        name: 'HelpRequests',
        component: HelpRequests
    },
    {
        path: '/agronomistHome/dailyPlan',
        name: 'DailyPlan',
        component: DailyPlan
    },
    {
        path: '/agronomistHome/writeReport',
        name: 'WriteReport',
        component: WriteReport
    },
    {
        path: '/ranking',
        name: 'RankPage',
        component: RankingView
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