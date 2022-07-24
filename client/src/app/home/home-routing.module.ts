import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {TaskPage} from './pages/task/task.page';
import {TasksPage} from './pages/tasks/tasks.page';

const routes: Routes = [
  {
    path: '',
    component: TasksPage,
  },
  
  {
    path: 'tasks',
    loadChildren: () => import('./pages/tasks/tasks.module').then( m => m.TasksPageModule)
  },
  {
    path: 'create-task',
    loadChildren: () => import('./pages/create-task/create-task.module').then( m => m.CreateTaskPageModule)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomePageRoutingModule {}
