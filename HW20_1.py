
# F I R S T   Q U E S T I O N

"""COALESCE in this case will change NULL value to 0
which means that if there is a course without students,
the answer of the query will be NULL, so the value of NULL will chang into 0
"""

##############################################
#DROP PROCEDURE IF EXISTS sp_update_courses_total;
"""
CREATE OR REPLACE FUNCTION sp_update_courses_total()
RETURNS TRIGGER AS $$
DECLARE
    grade real;  -- Variable to hold the grade
BEGIN
    -- Fetch the grade for the newly inserted student (if necessary)
    SELECT g.grade INTO grade
    FROM grades g
    WHERE g.student_id = NEW.student_id
    LIMIT 1;  -- Adjust if needed, depending on your data model (e.g., assuming one grade per student per course)

    -- Update the total number of students in the courses table
    UPDATE courses
    SET total_num_of_students = COALESCE((
        SELECT COUNT(DISTINCT student_id)
        FROM grades
        WHERE grades.course_id = NEW.course_id  -- Use NEW to reference the newly inserted row
    ), 0)
    WHERE course_id = NEW.course_id;

    RETURN NEW;  -- Return the new row to complete the INSERT operation
END;
$$ LANGUAGE plpgsql;
"""
###########################################################
"""
CREATE TRIGGER update_courses_total_trigger
AFTER INSERT ON grades
FOR EACH ROW
EXECUTE FUNCTION sp_update_courses_total();
"""
#second tringger on deleting a grade from grades
"""
CREATE OR REPLACE FUNCTION sp_update_courses_total()
RETURNS TRIGGER AS $$
DECLARE
    student_id int;  -- Variable to hold the grade
BEGIN
    -- Fetch the grade for the newly inserted student (if necessary)
    SELECT g.student_id INTO student_id
    FROM grades g
    WHERE g.student_id = old.student_id
    LIMIT 1;  -- Adjust if needed, depending on your data model (e.g., assuming one grade per student per course)

    -- Update the total number of students in the courses table
    UPDATE courses
    SET total_num_of_students = COALESCE((
        SELECT COUNT(DISTINCT grade)
        FROM grades
        WHERE grades.course_id = old.course_id  -- Use NEW to reference the newly inserted row
    ), 0)
    WHERE course_id = old.course_id;

    RETURN old;  -- Return the new row to complete the INSERT operation
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_courses_total_trigger
AFTER delete ON grades
FOR EACH ROW
EXECUTE FUNCTION sp_update_courses_total();

CREATE TRIGGER count_courses_total_trigger
AFTER delete ON grades
FOR EACH ROW
EXECUTE FUNCTION sp_update_courses_total();
"""

# S E C O N D  Q U E S T I O N
#first view
"""
CREATE VIEW all_grades_view AS
SELECT
    s.student_id,
    s.name as student_name,
    c.course_id,
    c.course_name,
    g.grade
   
FROM
    grades g
JOIN
    students s ON g.student_id = s.student_id
JOIN
    courses c ON g.course_id = c.course_id;

-- execute
select * from all_grades_view ;
1	Alice	3	Chemistry	88.0
1	Alice	5	History	56.0
1	Alice	6	Geography	82.0
1	Alice	7	Literature	78.0
1	Alice	8	Computer Science	59.0
2	Bob	1	Mathematics	87.0
2	Bob	3	Chemistry	81.0
2	Bob	4	Biology	56.0
2	Bob	5	History	90.0
3	Charlie	1	Mathematics	87.0
3	Charlie	3	Chemistry	96.0
3	Charlie	4	Biology	89.0
3	Charlie	6	Geography	77.0
3	Charlie	8	Computer Science	57.0
4	David	4	Biology	66.0
4	David	5	History	72.0
4	David	6	Geography	77.0
4	David	8	Computer Science	100.0
5	Eve	2	Physics	57.0
5	Eve	4	Biology	68.0
5	Eve	5	History	92.0
5	Eve	7	Literature	78.0
6	Frank	1	Mathematics	68.0
6	Frank	2	Physics	69.0
6	Frank	5	History	79.0
6	Frank	7	Literature	68.0
6	Frank	8	Computer Science	68.0
7	Grace	1	Mathematics	99.0
7	Grace	2	Physics	88.0
7	Grace	5	History	68.0
7	Grace	6	Geography	94.0
7	Grace	7	Literature	69.0
8	Hank	1	Mathematics	61.0
8	Hank	4	Biology	77.0
8	Hank	6	Geography	88.0
9	Ivy	1	Mathematics	57.0
9	Ivy	2	Physics	72.0
9	Ivy	4	Biology	94.0
9	Ivy	6	Geography	80.0
9	Ivy	7	Literature	79.0
9	Ivy	8	Computer Science	94.0
10	Jack	1	Mathematics	72.0
10	Jack	2	Physics	77.0
10	Jack	5	History	91.0
11	Kevin	2	Physics	70.0
11	Kevin	3	Chemistry	81.0
11	Kevin	6	Geography	64.0
11	Kevin	7	Literature	80.0
12	Laura	2	Physics	71.0
12	Laura	3	Chemistry	62.0
12	Laura	6	Geography	96.0
12	Laura	8	Computer Science	77.0
13	Michael	2	Physics	65.0
13	Michael	4	Biology	69.0
13	Michael	5	History	99.0
13	Michael	6	Geography	88.0
13	Michael	7	Literature	69.0
13	Michael	8	Computer Science	91.0
14	Nancy	1	Mathematics	56.0
14	Nancy	6	Geography	64.0
14	Nancy	7	Literature	81.0
14	Nancy	8	Computer Science	86.0
15	Oscar	2	Physics	83.0
15	Oscar	4	Biology	86.0
15	Oscar	6	Geography	60.0
16	Pam	1	Mathematics	68.0
16	Pam	2	Physics	72.0
16	Pam	3	Chemistry	69.0
16	Pam	5	History	83.0
17	Quinn	2	Physics	78.0
17	Quinn	3	Chemistry	81.0
17	Quinn	6	Geography	86.0
17	Quinn	7	Literature	96.0
18	Rick	1	Mathematics	63.0
18	Rick	3	Chemistry	59.0
18	Rick	4	Biology	56.0
18	Rick	5	History	68.0
18	Rick	7	Literature	98.0
19	Steve	4	Biology	86.0
19	Steve	5	History	85.0
19	Steve	6	Geography	85.0
19	Steve	7	Literature	100.0
19	Steve	8	Computer Science	60.0
20	Tina	3	Chemistry	76.0
20	Tina	4	Biology	66.0
20	Tina	6	Geography	67.0
20	Tina	7	Literature	80.0
21	Uma	2	Physics	60.0
21	Uma	3	Chemistry	95.0
21	Uma	4	Biology	69.0
21	Uma	6	Geography	69.0
21	Uma	8	Computer Science	57.0
22	Victor	1	Mathematics	97.0
22	Victor	3	Chemistry	90.0
22	Victor	4	Biology	66.0
22	Victor	5	History	83.0
22	Victor	6	Geography	87.0
22	Victor	7	Literature	66.0
23	Wendy	1	Mathematics	85.0
23	Wendy	2	Physics	63.0
23	Wendy	4	Biology	88.0
23	Wendy	5	History	94.0
23	Wendy	6	Geography	74.0
24	Xander	2	Physics	63.0
24	Xander	3	Chemistry	81.0
24	Xander	5	History	71.0
24	Xander	6	Geography	63.0
24	Xander	7	Literature	91.0
25	Yvonne	2	Physics	60.0
25	Yvonne	3	Chemistry	77.0
25	Yvonne	6	Geography	59.0
25	Yvonne	8	Computer Science	56.0
26	Zach	2	Physics	75.0
26	Zach	3	Chemistry	58.0
26	Zach	4	Biology	78.0
26	Zach	5	History	72.0
26	Zach	7	Literature	93.0
27	Amber	2	Physics	75.0
27	Amber	3	Chemistry	55.0
27	Amber	4	Biology	66.0
27	Amber	5	History	61.0
27	Amber	8	Computer Science	84.0
28	Bruce	2	Physics	83.0
28	Bruce	3	Chemistry	87.0
28	Bruce	6	Geography	78.0
28	Bruce	7	Literature	64.0
28	Bruce	8	Computer Science	78.0
29	Clara	1	Mathematics	93.0
29	Clara	2	Physics	68.0
29	Clara	3	Chemistry	68.0
29	Clara	4	Biology	57.0
29	Clara	6	Geography	72.0
29	Clara	7	Literature	89.0
4	David	2	Physics	70.0
4	David	1	Mathematics	80.0
"""
#second vieW
"""
CREATE VIEW over_eighty_grades_view AS
SELECT
    s.student_id,
    s.name as student_name,
    c.course_id,
    c.course_name,
    g.grade
   
FROM
    grades g
JOIN
    students s ON g.student_id = s.student_id
JOIN
    courses c ON g.course_id = c.course_id
 where g.grade > 80  ;

-- execute
select * from over_eighty_grades_view limit 10;
1	Alice	3	Chemistry	88.0
1	Alice	6	Geography	82.0
2	Bob	1	Mathematics	87.0
2	Bob	3	Chemistry	81.0
2	Bob	5	History	90.0
3	Charlie	1	Mathematics	87.0
3	Charlie	3	Chemistry	96.0
3	Charlie	4	Biology	89.0
4	David	8	Computer Science	100.0
5	Eve	5	History	92.0
"""
#Third view
"""
create
view
most_number_students_course_view as
select
c.course_id, c.course_name, c.total_num_of_students
from courses c

where
c.total_num_of_students =
(select max(total_num_of_students)
from courses)

select *
from most_number_students_course_view


6	Geography	21

"""
##############################################
#T H I R D  Q U E S T I O N
"""
drop function sp_most_successful_student;
CREATE or replace function sp_most_successful_student
(OUT student_name text, OUT average_grade double precision)
language plpgsql AS
    $$
        BEGIN
            SELECT s.name, s.course_avg_grades
            into student_name, average_grade
            from students s
            where s.course_avg_grades = (select max(course_avg_grades) from students);
        end;
    $$;

select * from sp_most_successful_student();

Quinn	85.25
"""



