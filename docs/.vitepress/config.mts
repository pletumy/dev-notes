import { defineConfig } from "vitepress";
import sidebar from "./sidebar.json";

export default defineConfig({
  title: "Dev Notes",
  description: "Ghi chú học tập cá nhân",
  lang: "vi",
  base: "/dev-notes/",

  themeConfig: {
    nav: [
      { text: "Home", link: "/" },
      { text: "Astro", link: "/astro/" },
    ],
    sidebar,
    search: {
      provider: "local",
    },
    outline: {
      level: [2, 3],
    },
  },
});
