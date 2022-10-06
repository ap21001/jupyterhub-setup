from traitlets import Unicode, List
from .base import BasePlugin from ..api import MissingEntry
class ExportPlugin(BasePlugin): """Base class for export plugins."""

to = Unicode("", help="destination to export to").tag(config=True)

student = List([],
    help="list of students to export").tag(config=True)

assignment = List([],
    help="list of assignments to export").tag(config=True)

def export(self, gradebook):
    """Export grades to another format.

    This method MUST be implemented by subclasses. Users should be able to
    pass the ``--to`` flag on the command line, which will set the
    ``self.to`` variable. By default, this variable will be an empty string,
    which allows you to specify whatever default you would like.

    Arguments
    ---------
    gradebook: :class:`nbgrader.api.Gradebook`
        An instance of the gradebook

    """
    raise NotImplementedError


class CsvExportPlugin(ExportPlugin): """CSV exporter plugin."""

def export(self, gradebook):
    if self.to == "":
        dest = "grades.csv"
    else:
        dest = self.to

    if len(self.student) == 0:
        allstudents = []
    else:
        # make sure studentID(s) are a list of strings
        allstudents = [str(item) for item in self.student]

    if len(self.assignment) == 0:
        allassignments = []
    else:
        # make sure assignment(s) are a list of strings
        allassignments = [str(item) for item in self.assignment]

    self.log.info("Exporting grades to %s", dest)
    if allassignments:
        self.log.info("Exporting only assignments: %s", allassignments)

    if allstudents:
        self.log.info("Exporting only students: %s", allstudents)

    fh = open(dest, "w")
    keys = [
        ##"assignment",
        ##"duedate",
        ##"timestamp",
        "student_id"
        ##"assignment"
        ##"last_name",
        ##"first_name",
        ##"email",
        ##"raw_score",
        ##"late_submission_penalty",
        ##"score",
        ##"max_score"
    ]
    fh.write(",".join(keys))
    fh.write(",")
    fmt = ",".join(["{" + x + "}" for x in keys])
    
    # Loop over each student in the database

    mode = 0
    mode2 = 0
    for student in gradebook.students:
        mode = 1
        print(student.id)
        # only continue if student is required
        if allstudents and student.id not in allstudents:
            continue

        # Loop over each assignment in the database
        if mode2 == 0:
            for assignment in gradebook.assignments:
                # only continue if assignment is required
                print(assignment.name)
                if allassignments and assignment.name not in allassignments:
                    continue
                
                keys = [
                str(assignment.name)
                ]
                fh.write(",".join(keys))
                fh.write(",")
                fmt = ",".join(["{" + x + "}" for x in keys]) #+ "\n"
            mode2 = 1
            fh.write("\n")

        for assignment in gradebook.assignments:
            # only continue if assignment is required
            if allassignments and assignment.name not in allassignments:
                continue

            # Create a dictionary that will store information 
            # about this student's submitted assignment
            score = {}
            ##score['score'] = assignment.score
            ##print(assignment.name + str(score[assignment.name])) #+ str(score))
            ##score['assignment'] = assignment.name
            score['student_id'] = student.id
            ##print(str(score['student_id']))
            ##score['assignment'] = assignment.name
            ##score['last_name'] = student.last_name
            ##score['first_name'] = student.first_name
            ##score['max_score'] = assignment.max_score

            try:
                submission = gradebook.find_submission(
                    assignment.name, student.id)
                ##print(submission)
                ##print(str(score))
            except MissingEntry:
                ##score['score'] = 0.0
                score[assignment.name] = 0.0
            else:
                penalty = submission.late_submission_penalty
                ##score['score'] = max(0.0, submission.score - penalty)
                score[assignment.name] = max(0.0, submission.score - penalty)
            for key in score:
                if score[key] is None:
                    score[key] = ''
                if not isinstance(score[key], str):
                    score[key] = str(score[key])
        
            ##print(submission)
            ##print(str(score))
            if mode == 1:
                fh.write(score['student_id'])
                fh.write(",")
                fh.write(score[assignment.name])
                fh.write(",")
                mode += 1
            ##fh.write(fmt.format(**score))
            else:
                fh.write(score[assignment.name])
                fh.write(",")
        mode = 0
        fh.write("\n")
    fh.close()