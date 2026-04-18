import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('../components/layout/AppLayout.vue'),
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('../views/DashboardView.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'classes',
        name: 'classes',
        component: () => import('../views/ClassListView.vue'),
        meta: { title: '班级管理' }
      },
      {
        path: 'classes/:id',
        name: 'class-detail',
        component: () => import('../views/ClassDetailView.vue'),
        meta: { title: '班级详情' }
      },
      {
        path: 'children/:id',
        name: 'child-profile',
        component: () => import('../views/ChildProfileView.vue'),
        meta: { title: '幼儿档案' }
      },
      {
        path: 'anecdotes/new',
        name: 'anecdote-new',
        component: () => import('../views/AnecdoteFormView.vue'),
        meta: { title: '新建观察记录' }
      },
      {
        path: 'anecdotes/:id/edit',
        name: 'anecdote-edit',
        component: () => import('../views/AnecdoteFormView.vue'),
        meta: { title: '编辑观察记录' }
      },
      {
        path: 'anecdotes',
        name: 'anecdotes',
        component: () => import('../views/AnecdoteListView.vue'),
        meta: { title: '观察记录' }
      },
      {
        path: 'assessments',
        name: 'assessments',
        component: () => import('../views/AssessmentListView.vue'),
        meta: { title: '阶段性评估' }
      },
      {
        path: 'assessments/:id',
        name: 'assessment-detail',
        component: () => import('../views/AssessmentDetailView.vue'),
        meta: { title: '评估详情' }
      },
      {
        path: 'compare',
        name: 'compare',
        component: () => import('../views/HistoryCompareView.vue'),
        meta: { title: '历史对比' }
      },
      {
        path: 'system',
        name: 'system',
        component: () => import('../views/SystemView.vue'),
        meta: { title: '系统管理' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '幼儿发展评估系统'} - 幼儿发展评估系统`
  next()
})

export default router
