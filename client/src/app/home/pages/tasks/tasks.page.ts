import { Component, OnInit } from '@angular/core';
import { Task, TaskService, Workers } from 'src/app/services/tasks/task.service';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.page.html',
  styleUrls: ['./tasks.page.scss'],
})
export class TasksPage implements OnInit {

  private tasks: Task[];

  constructor(private service: TaskService) {}

  ngOnInit() {
    this.service.getTasks().subscribe((res) => {
      console.log(res)
      this.tasks = res
    });
  }

  refresh(ev) {
    setTimeout(() => {
      ev.detail.complete();
    }, 3000);
  }
}
