import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import "ace-builds/webpack-resolver";
import "brace/mode/python";
import "brace/theme/monokai";
import {EditorService} from "../services/editor.service";

@Component({
  selector: 'code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls: ['./code-editor.component.css']
})
export class CodeEditorComponent implements OnInit, AfterViewInit {
  @ViewChild('editor') editor;
  code = '';

  private readonly options = {
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    fontSize: 18,
  };

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

}
