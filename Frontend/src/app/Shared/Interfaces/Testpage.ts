export interface MCQQuestion {
  question: string;
  'option 1': string;
  'option 2': string;
  'option 3': string;
  'option 4': string;
  answer: string;
  user_answer?: string;
}

export interface TFQuestion {
  question: string;
  'option 1': string;
  'option 2': string;
  answer: string;
  user_answer?: string;
}

export interface FillInTheBlankQuestion {
  question: string;
  answer: string;
  user_answer?: string;
}

export interface ScenarioQuestion {
  question: string;
  user_answer?: string;
}

export interface PersonData {
  mcq: MCQQuestion[];
  'true/false': TFQuestion[];
  'fill in the blanks': FillInTheBlankQuestion[];
  scenario: ScenarioQuestion[];
}

export interface QuestionsResponse {
  people: number;
  [key: string]: any;
}

export interface UserAnswersData {
  mcq: string[];
  'true/false': string[];
  'fill in the blanks': string[];
  scenario: string[];
}