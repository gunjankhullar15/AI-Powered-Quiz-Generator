export interface TestForm {
  name: string;
  numMCQ: string;
  numMatchFollowing: string;
  numScenarioBased: string;
  numFillBlanks: string;
  numTrueFalse: string;
  duration: string;
  deadline: string;
  passingMarks: number;
  totalMarks: number;
  numPeople: string;
  description: string;
  document: File | null;
  articleLink: string;
  topic: string;
}

export interface WeightageResponse {
  question_type: string;
  weightage: string;
  w_id: number;
}

export interface MarksConfig {
  mcq: number;
  matchFollowing: number;
  scenarioBased: number;
  fillBlanks: number;
  trueFalse: number;
}



export interface CreateTestPayload {
  topic: string;
  test_name: string;
  description: string;
  due_date: string;
  no_of_mcq: number;
  no_scenario_based: number;
  no_of_fill_blanks: number;
  no_of_true_false: number;
  duration: number;
  max_marks: number;
  passing_marks: number;
  no_of_people: number;
  created_at: string;
}

export interface CreateTestResponse {
  success?: boolean;
  message?: string;
  test_id?: string;
  testLink?: string;
  link?: string;
  url?: string;
  test_link?: string;
  test_url?: string;
}

export interface DocumentPreviewResponse {
  success: boolean;
  data?: any;
  message?: string;
}
