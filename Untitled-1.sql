USE master
GO
IF NOT EXISTS (
   SELECT name
   FROM sys.databases
   WHERE name = N'Profile Type'
)
CREATE DATABASE [Profile Type]
GO
-- Create a new table called 'Students' in schema 'SchemaName'
-- Drop the table if it already exists
IF OBJECT_ID('SchemaName.Students', 'U') IS NOT NULL
DROP TABLE SchemaName.Students
GO
-- Create the table in the specified schema
CREATE TABLE SchemaName.Students
(
    StudentsId INT NOT NULL PRIMARY KEY, -- primary key column
    id [NVARCHAR](50) NOT NULL,
    names[NVARCHAR](50) NOT NULL,
    age [NVARCHAR](50) NOT NULL,  
    country  [NVARCHAR](50) NOT NULL, 
    states  [NVARCHAR](50) NOT NULL,
    intrest [NVARCHAR](50) NOT NULL,
    teachers[NVARCHAR](50) NOT NULL, 
    /*many to many for teaachers*/
      -- specify more columns here
);
GO 
/* chat window
 */
-- Create a new table called 'Mentor' in schema 'SchemaName'
-- Drop the table if it already exists
IF OBJECT_ID('SchemaName.Mentor', 'U') IS NOT NULL
DROP TABLE SchemaName.Mentor
GO
-- Create the table in the specified schema
CREATE TABLE SchemaName.Mentor
(
    MentorId INT NOT NULL PRIMARY KEY, -- primary key column
     id [NVARCHAR](50) NOT NULL,
    names[NVARCHAR](50) NOT NULL,
    age [NVARCHAR](50) NOT NULL,  
    company [NVACHAR](50) NOT NULL,
    country  [NVARCHAR](50) NOT NULL, 
    states  [NVARCHAR](50) NOT NULL,
    intrest [NVARCHAR](50) NOT NULL,
    students [NVARCHAR](50) NOT NULL 
     /*many to many for students*/ 
    -- specify more columns here
);
GO 
/*intrest pseudo code */ 
 /* intrest=["Sceince","History", "Math"]
 enter 1 for intrest[0]...
*/ 