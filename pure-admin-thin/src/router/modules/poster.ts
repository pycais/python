export default {
  path: "/poster",
  redirect: "/poster/data-list",

  meta: {
    icon: "ri:information-line",
    title: "豆瓣图片",
    rank: 44
  },
  children: [
    {
      path: "/poster/data-list",
      name: "PosterDataList",
      component: () => import("@/views/poster/index.vue"),
      meta: {
        title: "豆瓣图片"
      }
    },
    {
      path: "/poster/data-first",
      name: "PosterDataFirst",
      component: () => import("@/views/poster/index.vue"),
      meta: {
        title: "豆瓣图片2"
      }
    }
  ]
} satisfies RouteConfigsTable;
