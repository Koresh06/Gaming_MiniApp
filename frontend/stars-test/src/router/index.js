import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },

  {
    path: "/game/:code",
    name: "Game",
    component: () => import("../views/Game.vue"),
  },

  // 🔥 ВАЖНО: ловим ВСЁ остальное от Telegram
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
