import { Component, Input, OnInit } from '@angular/core';
import {Task, TaskService} from 'src/app/services/tasks/task.service';

@Component({
  selector: 'app-task-item',
  templateUrl: './task-item.component.html',
  styleUrls: ['./task-item.component.scss'],
})
export class TaskItemComponent implements OnInit {

  @Input() task: Task;

  constructor(private service: TaskService) { }

  ngOnInit() {}

  delete(){ 
    this.service.del(this.task.id).subscribe( res => { 
      console.log(res)
    } );
  }

}
