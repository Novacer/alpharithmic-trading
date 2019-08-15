import {AfterViewInit, Component, EventEmitter, OnInit, Output, ViewChild} from '@angular/core';
import 'ace-builds/webpack-resolver';
import 'brace/mode/python';
import 'brace/theme/monokai';
import {EditorService} from '../services/editor.service';

@Component({
  selector: 'code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent implements OnInit, AfterViewInit {

  private readonly options = {
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    fontSize: 18,
  };

  @ViewChild('editor') editor;
  @Output() codeChangeEvent = new EventEmitter<string>();
  code = '';

  constructor(private editorService: EditorService) { }

  ngOnInit() {
    this.editorService.getDefaultSrcCode().subscribe(response => {
      this.code = response;
    });
  }

  ngAfterViewInit() {
    this.editor.setTheme('monokai');
    this.editor.setMode('python');

    this.editor.getEditor().setOptions(this.options);
  }

  emitCodeChangedEvent(code: string) {
    this.codeChangeEvent.emit(code);
  }
}
