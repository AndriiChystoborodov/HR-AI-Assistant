import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AssistantService } from '../../services/assistant.service';
import packageInfo from '../../../../package.json';


@Component({
  selector: 'app-assistant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './assistant.component.html',
  styleUrl: './assistant.component.css'
})
export class AssistantComponent {
  private assistantService = inject(AssistantService);

  question = '';
  loading = false;
  lastQuestion = '';

  messages: { role: string; text: string }[] = [];
  version = packageInfo.version;

  // Hardcoded most frequent questions
  suggestedQuestions = [
    '📅 What are the Swiss public holidays this year?',
    '💼 What are the company expense policies?',
    '❓ How do I request time off?'
  ];

  submit() {
    if (!this.question.trim()) return;
    this.submitQuestion(this.question);
  }

  submitQuestion(text: string) {
    this.lastQuestion = text;
    this.question = '';
    this.loading = true;

    this.messages.push({ role: 'user', text });
    this.messages.push({ role: 'bot', text: 'Thinking...' });

    this.assistantService.ask(text).subscribe({
      next: (res: { answer: string }) => {
        // Remove "Thinking..." message
        this.messages.pop();

        // Add answer
        this.messages.push({
          role: 'bot',
          text: res.answer
        });

        this.loading = false;
      },
      error: (err: unknown) => {
        console.error(err);

        // Remove "Thinking..." message
        this.messages.pop();

        this.messages.push({
          role: 'bot',
          text: 'Error calling backend'
        });

        this.loading = false;
      }
    });
  }

  retryLast() {
    if (this.lastQuestion.trim() && !this.loading) {
      this.submitQuestion(this.lastQuestion);
    }
  }

  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.submit();
    }
  }
}


