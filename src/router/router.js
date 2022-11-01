import Vue from 'vue'
import VueRouter from 'vue-router'
import Booking from '../components/Booking.vue'
import CreateSlot from '../components/CreateSlot.vue'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Inventory from '../components/Inventory.vue'
import AdminPanel from  '../components/AdminPanel'
import UserPanel from '../components/UserPanel'
import Session from '../components/Session'
import Users from '../components/Users.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
import ResetPassword from '../components/ResetPassword.vue'
import NotFound from '../components/Errors/404'
import E403 from '../components/Errors/403'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      isAuthenticated: true
    }
  },

  {
    path: '/booking',
    name: 'Booking',
    component: Booking,
    meta: {
      isAuthenticated: true
    }
  },

  {
    path: '/createSlot',
    name: 'CreateSlot',
    component: CreateSlot,
    meta: {
      isAuthenticated: true,
      requiresAdmin: true
    }
  },

  {
    path: '/login',
    name: 'Login',
    component: Login
  },

  {
    path: '/register',
    name: 'Register',
    component: Register
  },

  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory,
    meta: {
      isAuthenticated: true,
      requiresAdmin: true
    }
  },

  {
    path: '/user-panel',
    name: 'UserPanel',
    component: UserPanel,
    meta: {
      isAuthenticated: true
    }
  },

  {
    path: '/user-panel/:session',
    name: 'Session',
    component: Session,
    meta: {
      isAuthenticated: true
    }
  },
  
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: {
      isAuthenticated: true,
      requiresAdmin: true
    }
  },

  {
    path: '/admin-panel',
    name: 'AdminPanel',
    component: AdminPanel,
    meta: {
      isAuthenticated: true,
      requiresAdmin: true
    }
  },
  {
    path: '/forgot',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: {
      isAuthenticated: false
    }
  },
  {
    path: '/password_reset/:token',
    name: 'ResetPassword',
    component: ResetPassword,
    meta: {
      isAuthenticated: false
    }
  },
  { 
    path: '*', beforeEnter: (to, from, next) => { next('/404') } },
  {
    path: "/404",
    name: '404',
    component: NotFound
  },
  {
    path: "/403",
    name: '403',
    component: E403
  }
]

const router = new VueRouter({
  //mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem("user"));
  if (to.matched.some(r => r.meta.isAuthenticated)) {
    if (user == null) {
      // The page is protected and the user is not authenticated. Force a login.
      next('/login');
    }
    if (to.meta.requiresAdmin && (user.role !== "ROLE_ADMIN")) {
      // reject access to admin routes for regular users
      next('/403')
    }
    else {     
      next()
    }
  } else {
    // This page did not require authentication
    next()
  }
})

export default router