import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AssistantService {
  private http = inject(HttpClient);

  ask(question: string): Observable<{ answer: string }> {
    return this.http.post<{ answer: string }>('https://guided-project-greenleaf-smart-ops-ital.onrender.com/ask', {
      question
    });
  }
}