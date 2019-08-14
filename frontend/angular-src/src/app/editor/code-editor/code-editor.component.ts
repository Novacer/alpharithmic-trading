import {AfterViewInit, Component, ViewChild} from '@angular/core';
import "ace-builds/webpack-resolver";
import "brace/mode/python";
import "brace/theme/monokai";

@Component({
  selector: 'code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent implements AfterViewInit {
  @ViewChild('editor') editor;
  code = 'print("Hello World!")';

  private readonly options = {
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    fontSize: 18,
  };

  constructor() { }

  ngAfterViewInit() {
    this.editor.setTheme('monokai');
    this.editor.setMode('python');

    this.editor.getEditor().setOptions(this.options);
  }

}
