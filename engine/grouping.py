import operator
from itertools import groupby

reverse = False

class Student:
    def __init__(self, id, name, grade, gender, specialisation, foreigner=""):
        self.id = id
        self.name = name
        self.grade = grade
        self.gender = gender
        self.foreigner = foreigner
        self.specialisation = specialisation

    def __repr__(self):
        return repr((self.id, self.name, self.grade, self.gender, self.foreigner, self.specialisation))

def reverse_sort():
    global reverse
    reverse = not reverse
    return reverse

def perform_grouping(param_students_data, param_number_of_groups):
    students = []

    for d in param_students_data:
        id = d[0]
        name = d[1]
        country = d[2]
        gender = d[3]
        grade = d[4]
        specialty = d[5]
        students.append(Student(id,name,grade,gender,specialty,country))

    NUMBER_OF_GROUPS = param_number_of_groups
    groups = [[] for i in range(NUMBER_OF_GROUPS)]
    counter = 0

    gender_attr = operator.attrgetter("gender")
    grade_attr = operator.attrgetter("grade")
    natinal_attr = operator.attrgetter("foreigner")
    spe_attr = operator.attrgetter("specialisation")

    grouped_students = []
    # Group by national
    for national_key, national_vals in groupby(sorted(students, key=grade_attr), gender_attr):
        grouped_students.append(
            [
                [
                    list(grade_vals)
                    # Group by grade
                    for grade_key, grade_vals in groupby(sorted(gender_vals, key=natinal_attr), natinal_attr)
                ]
                # Group by gender
                for gender_key, gender_vals in groupby(sorted(national_vals, key=gender_attr), grade_attr)
            ]
        )

    for gender_group in grouped_students:
        for national_group in gender_group:
            for specialisation_group in national_group:
                for student in sorted(specialisation_group, key=spe_attr, reverse=reverse_sort()):
                    groups[counter].append(student)
                    counter = (counter + 1) % NUMBER_OF_GROUPS
    
    #return groups
    print_group(groups)

def print_group(student_groups):
    for i in range(len(student_groups)):
        print("Group {0}:".format(i + 1))
        for member in student_groups[i]:
            print(member)

def optimize(groups):
    pass 

def get_data():
    data = [
            (1279, 'A Audu', '', '', 'A', 'X (Prov)'), 
            (1342, 'AJ Dyeri', '', '', 'C-', 'X (Prov)'), 
            (1295, 'AO Olatunji', '', '', 'B', 'Log (Proj)'), 
            (1277, 'AR Sule', '', '', '', 'Med (Physio)'),
            (1351, 'B Gambo', '', '', 'C', 'X (AWW)'), 
            (1336, 'B George', '', '', 'C', 'Edn'), 
            (1370, 'C       Okoro', '', '', 'B-', 'X (CIT) '), 
            (1290, 'FE Wakili', '', '', 'B+', 'X (ND)'), 
            (1341, 'GN Odo', '', '', 'F', 'Edn '), 
            (1306, 'I Orumabo', '', '', 'B-', 'Log (Proc)'), 
            (1362, 'JC Chabanga', 'Botswana', '', 'C', 'Edn'), 
            (1328, 'MA David', '', '', 'B', 'X (AWW)'), 
            (1301, 'NM Mustapha', '', '', 'F', 'X(Comms)'), 
            (1343, 'NY Suleiman', '', '', 'B', 'Edn'), 
            (1355, 'OI Obetta', '', '', 'B', 'X (ND)'), 
            (1337, 'OU Balogun', '', '', 'F', 'Log (Proj)'), 
            (1325, 'U Ando', '', '', 'C', 'X(Comms)'), 
            (1278, 'US Abdullahi', '', 'F', 'HC', 'Edn '), 
            (1275, 'YB Mohammed', '', '', 'B+', 'Med (Lab)'), 
            (1365, 'ZK Assouma', 'Benin', '', 'B', 'X (Prov)'), 
            (1321, 'A Arogundade', '', 'F', 'F', 'A & B'), 
            (1311, 'AA Ikoro', '', '', 'B+', 'Log (Log)'), 
            (1304, 'AA Jimoh', '', '', 'C-', 'X (AWW)'), 
            (1339, 'AG Gada', '', '', 'C', 'Edn'), 
            (1331, 'BB Brown', '', '', 'C', 'NEB (WEE/AE)'), 
            (1288, 'FA Francis', '', '', 'B-', 'X (AWW)'), 
            (1334, 'HS Waja', '', '', 'B', 'Log (Proj)'), 
            (1333, 'IJ Galaki', '', '', 'B-', 'Log (Proc)'), 
            (1348, 'J Mudi', '', '', 'B', 'X (Legal)'), 
            (1300, 'JT Bere', '', '', 'LC', 'X(Comms) '), 
            (1323, 'K Abdullahi', '', '', 'B', 'A&B'), 
            (1344, 'KK Kachiro', '', '', 'B', 'NEB (WEE/AE)'), 
            (1294, 'KR Elero', '', '', 'B+', 'X (AWW)'), 
            (1352, 'MD Abba', '', '', 'F', 'A & B'), 
            (1305, 'NP Ochasi', '', '', 'A', 'X(Comms)'), 
            (1329, 'PA Adewunmi', '', '', 'C', 'X(Comms)'), 
            (1276, 'RS Wakama', '', '', '', 'Edn'), 
            (1364, 'T Ganakgomo', 'Botswana', '', 'B', 'Edn '), 
            (1359, 'TV Ramapulane', 'S/Africa', '', 'C', 'Edn'), 
            (1296, 'UI Urang', '', '', 'F', 'X (UWW)'), 
            (1361, 'A Banasco', 'Ghana', '', 'B', 'Med (Lab)'), 
            (1368, 'A Bojang', 'The Gambia', '', 'C', 'Edn'), 
            (1283, 'AS Jega', '', '', 'C-', 'NEB (WEE/AE)'), 
            (1332, 'AS Tasunda', '', '', 'F', 'NEB (ME)'), 
            (1358, 'BK Kamara', 'S/Leone', '', 'B+', 'Log (Log)'), 
            (1302, 'BY Ahmed', '', '', 'B+', 'NEB (WE)'), 
            (1371, 'DO    Adebesin', '', '', 'B', 'X (Legal)'), 
            (1319, 'EJ Itemuagbor', '', '', 'B', 'Log (Proj)'), 
            (1317, 'M Iliya', '', '', 'B-', 'A & B'), 
            (1309, 'MA Salihu', '', '', 'C', 'Log (Proc)'), 
            (1369, 'MD    Nestor', 'Chad', '', 'F', 'NEB (WEE/AE)'), 
            (1293, 'MY Shimfe', '', '', 'A', 'A & B'), 
            (1307, 'NA Alkali', '', '', 'B', 'NEB (WEE/AE)'), 
            (1280, 'OO Fagbola', '', '', 'LC', 'Edn'), 
            (1324, 'OO Ogunrinde', '', '', 'B', 'X(Comms) '), 
            (1299, 'S Miller', '', '', 'B', 'A&B'), 
            (1281, 'SA Olokopo', '', '', 'B-', 'NEB (WEE/AE)'), 
            (1345, 'SI Obiefuna', '', '', 'C', 'Edn'), 
            (1303, 'SK Shekarau', '', '', 'F', 'X (Pilot)'), 
            (1320, 'Y Ahmed', '', '', 'C', 'X (UWW)'), 
            (1353, 'AD Abdullahi', '', '', 'B-', 'X (ND)'), 
            (1350, 'AL Idowu', '', '', 'B', 'X (UWW)'), 
            (1289, 'EM Ukande', '', '', 'B', 'A & B'), 
            (1291, 'FC Aya', '', '', 'HC', 'Log (Prov)'), 
            (1340, 'FM Okolo', '', '', 'F', 'Med (Physio)'), 
            (1347, 'FO Arikpo', '', '', 'B', 'X (CIT) '), 
            (1287, 'H Nalado', '', '', 'C', 'X (UWW)'), 
            (1315, 'I Mustapha', '', '', 'C-', 'Log (Prov)'), 
            (1274, 'IAM  Enemakwu', '', '', 'B+', 'Med (Surg)'), 
            (1297, 'M Hamadikko', '', '', 'C', 'A & B'), 
            (1360, 'MM   Rabiou', 'Niger', '', 'B', 'Log (Proj)'), 
            (1314, 'NM Nworah', '', '', 'F', 'X (ND)'), 
            (1356, 'OJ Osoba', '', '', 'C', 'Log (Proc)'), 
            (1346, 'OO Bamikole', '', '', 'B-', 'NEB (WEE/AE)'), 
            (1308, 'PE Enai', '', '', 'B', 'NEB (ME)'), 
            (1322, 'PI Yusuf', '', '', 'B-', '(NEB WEE)'), 
            (1366, 'PTK Patatchona', 'Togo', '', 'C', 'Edn'), 
            (1284, 'U Adamu', '', '', 'A', 'X (CIT) '), 
            (1330, 'U Tukur', '', '', 'B', 'Log (Proc)'), 
            (1312, 'A Buhari', '', '', 'C', 'Edn'), 
            (1335, 'A Enias', '', '', 'B', 'Log (Log)'), 
            (1292, 'A Onyeukwu', '', '', 'C', 'X (ND)'), 
            (1313, 'A Tsalha', '', 'F', 'F', 'Log (Proj)'), 
            (1354, 'AK Balarabe', '', '', 'B', 'Log (Prov)'), 
            (1327, 'AO Adewara', '', '', 'B', 'X (Pilot)'), 
            (1357, 'AY Nguide', '', '', 'F', 'Log (Proj)'), 
            (1338, 'CC Nwosu', '', '', 'B+', 'Med (Lab)'), 
            (1282, 'D Sikiru', '', 'F', 'C+', 'Edn'), 
            (1349, 'EG Usibe', '', '', 'C', 'A & B'), 
            (1298, 'GS Monde', '', '', 'HC', '(NEB WEE)'), 
            (1310, 'GY Mohammed', '', '', 'F', 'Log (Proj)'), 
            (1318, 'MH Gombe', '', '', 'B', 'X (AWW)'), 
            (1286, 'NI Nkanang', '', '', 'B', ''), 
            (1367, 'P Kamingh', 'Togo', '', 'B', 'NEB (WEE/AE)'), 
            (1285, 'SA Ekundayo', '', '', 'B-', 'X (Legal)'), 
            (1316, 'TT Paave', '', '', 'A', 'X (ND)'), 
            (1326, 'UJ Barau', '', '', 'B-', 'NEB (WE)'), 
            (1363, 'W Bashaija', 'Rwanda', '', 'B-', 'Med (Physio)')
        ]
    
    return (data)

data = get_data()
number_of_groups = 5
perform_grouping(data, number_of_groups)