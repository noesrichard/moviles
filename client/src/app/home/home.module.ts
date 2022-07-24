import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { HomePageRoutingModule } from './home-routing.module';
import {TaskPage} from './pages/task/task.page';
import {TasksPage} from './pages/tasks/tasks.page';
import {TaskItemComponent} from './components/task-item/task-item.component';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    HomePageRoutingModule
  ],
  declarations: [TaskPage, TasksPage, TaskItemComponent]
})
export class HomePageModule {}
