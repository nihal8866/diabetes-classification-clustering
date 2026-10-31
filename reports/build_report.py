from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect, Line, String

ROOT = Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('TNR', 'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('TNR-Bold', 'C:/Windows/Fonts/timesbd.ttf'))
pdfmetrics.registerFontFamily('TNR', normal='TNR', bold='TNR-Bold', italic='TNR', boldItalic='TNR-Bold')
body = ParagraphStyle('Body', fontName='TNR', fontSize=11, leading=14, spaceAfter=9, textColor=colors.black)
heading = ParagraphStyle('Heading', parent=body, fontName='TNR-Bold', fontSize=17, leading=21, spaceBefore=12, spaceAfter=10, keepWithNext=True)
title = ParagraphStyle('Title', parent=heading, fontSize=18, leading=23, alignment=TA_CENTER, spaceAfter=12)
small = ParagraphStyle('Table', parent=body, fontSize=10.5, leading=13, spaceAfter=0)
story = []
table_number = 0
table_titles = ['Class distribution after label normalization', 'Grouped training and test class counts', 'Grouped cross validation classifier comparison', 'Held out classification metrics', 'Known classes within each K means cluster', 'Selected median measurements by cluster', 'Misclassified held out records']
def p(text): story.append(Paragraph(text, body))
def h(text): story.append(Paragraph(text, heading))
def table(rows, widths=None):
    global table_number
    table_number += 1
    story.append(Paragraph(f'Table {table_number}  {table_titles[table_number-1]}', ParagraphStyle('Caption',parent=body,fontSize=10.5,leading=13,keepWithNext=True)))
    data = [[Paragraph(('<b>'+str(v)+'</b>') if i == 0 else str(v), small) for v in row] for i,row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LINEBELOW',(0,0),(-1,0),0.5,colors.black),
        ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
    ]))
    story.extend([t, Spacer(1,10)])
def page(): story.append(PageBreak())

cover = ParagraphStyle('Cover',parent=body,alignment=TA_CENTER,fontSize=12,leading=17)
story.append(Spacer(1,95))
story.append(Paragraph('ASSOCIATE ML ENGINEER', ParagraphStyle('CoverRole',parent=cover,fontSize=12,spaceAfter=28)))
story.append(Paragraph('Diabetes Classification<br/>and Clustering', ParagraphStyle('CoverTitle',parent=title,fontSize=28,leading=34,spaceAfter=18)))
story.append(Paragraph('Take Home Assignment Report', ParagraphStyle('CoverSubtitle',parent=cover,fontSize=15,leading=20)))
story.append(Spacer(1,50))
story.append(Paragraph('Prepared by',cover))
story.append(Paragraph('Nihal Mahato', ParagraphStyle('CoverAuthor',parent=cover,fontName='TNR-Bold',fontSize=18,leading=23)))
story.append(Spacer(1,43))
story.append(Paragraph('Project Repository', ParagraphStyle('RepositoryLabel',parent=cover,fontName='TNR-Bold',spaceAfter=8)))
story.append(Paragraph('<link href="https://github.com/nihal8866/diabetes-classification-clustering" color="black">github.com/nihal8866/<br/>diabetes-classification-clustering</link>',cover))
story.append(Spacer(1,43))
story.append(Paragraph('October 2026',cover))
page()
story.append(Paragraph('Table of Contents', title))
story.append(Spacer(1,20))
toc = TableOfContents()
toc.levelStyles = [ParagraphStyle('TOC',fontName='TNR',fontSize=12,leading=17,spaceBefore=9,textColor=colors.black)]
story.append(toc)
story.append(Spacer(1,35))
p('Figures: training measurement distributions and held out confusion matrix. Seven numbered tables summarize the data, evaluation, clusters, and errors.')
page()
h('1 Objective and main findings')
p('This project examines a 1,000-record diabetes dataset using supervised classification and unsupervised clustering. The classification task predicts the supplied N, P, or Y label from patient attributes. The clustering task explores whether similar records form groups that resemble those labels.')
p('Random forest was selected over logistic regression using grouped cross-validation macro-F1. On the reserved 201-record test set it achieved accuracy of 0.985 and macro-F1 of 0.973, with three errors. K-means with three clusters produced a training silhouette score of 0.183 and adjusted Rand index of 0.572. Its groups partially agreed with the classes but did not reproduce them exactly. Uncertain patient identity and the small P test sample limit the strength of these findings.')
h('2 Dataset and exploratory analysis')
p('The spreadsheet contains 14 columns: ID, No_Pation, Gender, AGE, Urea, Cr, HbA1c, Chol, TG, HDL, LDL, VLDL, BMI, and CLASS. ID and No_Pation were treated as identifiers and excluded from model inputs. CLASS was retained as the target. The remaining 11 columns comprise ten numeric measurements and Gender. Labels are used as supplied; the assignment describes N as non-diabetic, Y as diabetic, and P as Predict-diabetic.')
table([['Class','Count','Share'],['N',103,'10.3%'],['P',53,'5.3%'],['Y',844,'84.4%']], [180,130,140])
p('Pandas detected no missing values, but this does not rule out undocumented missing-value codes. One lowercase gender value was standardized, and surrounding spaces were removed from Gender and CLASS. This merged N with N-space and Y with Y-space without deleting records. Raw data and the original loaded table were preserved.')
p('The initial audit found no exact duplicate rows across all columns, but 174 repeated records after the first occurrence when identifiers were excluded. There were 826 distinct feature combinations and no conflicting labels within identical feature groups. ID had 800 unique values and No_Pation had 961. Repeated identifiers sometimes had different measurements, so neither was assumed to establish patient identity.')

page()
story.append(Paragraph('Training data distributions', heading.clone('FigureHeading')))
p('Figure 1 shows the ten numeric input features for the 799 training records. Each panel uses 20 equal width bins. Axes retain original dataset units; measurement units have not been independently verified. All bars and text are black.')
hist_data = json.loads((ROOT/'figures/training_histograms.json').read_text(encoding='utf-8'))
d = Drawing(450,490)
for i,(name,values) in enumerate(hist_data.items()):
    x=35+(i%2)*230; y=405-(i//2)*98
    w=175; ht=60; counts=values['counts']; edges=values['edges']; top=max(counts)
    d.add(String(x+w/2,y+ht+12,name,fontName='TNR-Bold',fontSize=10,textAnchor='middle',fillColor=colors.black))
    d.add(Line(x,y,x+w,y,strokeColor=colors.black,strokeWidth=.5))
    d.add(Line(x,y,x,y+ht,strokeColor=colors.black,strokeWidth=.5))
    for j,count in enumerate(counts):
        if count: d.add(Rect(x+j*w/20,y,w/20-.3,ht*count/top,fillColor=colors.black,strokeColor=None))
    for value,labelx,anchor in [(edges[0],x,'start'),(edges[-1],x+w,'end')]:
        d.add(String(labelx,y-11,f'{value:g}',fontName='TNR',fontSize=8,textAnchor=anchor,fillColor=colors.black))
    d.add(String(x-5,y+ht-3,str(top),fontName='TNR',fontSize=8,textAnchor='end',fillColor=colors.black))
    d.add(String(x-5,y-2,'0',fontName='TNR',fontSize=8,textAnchor='end',fillColor=colors.black))
story.append(d)
p('Figure 1  Training data histograms. Horizontal axes show measurement values and vertical axes show record counts. Long right tails are especially visible for Cr, HDL, and VLDL. These patterns motivate scaling but do not establish that extreme values are invalid.')

page()
h('3 Numeric findings and preprocessing')
p('Training-data histograms showed pronounced right tails for Cr, HDL, and VLDL, with right skew also visible in Urea and TG. Numeric inspection flagged one Chol value of zero, Cr values up to 800, HDL up to 9.9, VLDL up to 35, and HbA1c as low as 0.9. These are investigation flags rather than confirmed errors. Units and source records were not independently verified, so no clinical thresholds, guessed corrections, or automatic outlier deletions were applied.')
p('The initial implementation retains all numeric values. StandardScaler transforms the ten numeric measurements using training means and standard deviations. OneHotEncoder converts Gender into F and M indicators, with unknown categories ignored during transformation. This produces 12 transformed features. Scaling changes units but does not remove extreme observations; those observations can still influence distance-based clustering.')
p('A ColumnTransformer combines the two preprocessing branches. Each classifier is wrapped in a Pipeline so cross-validation learns preprocessing separately within each fold. Illustrative transformations fitted on the whole training set were not supplied as precomputed inputs to cross-validation. Tree models do not require standard scaling, but the same transformation was retained for a consistent initial implementation.')
h('4 Evaluation design')
p('An ordinary row-level random split could place identical inputs in both training and test data. To prevent this, rows were grouped by all 11 input features, excluding identifiers and CLASS. The first split from StratifiedGroupKFold with five folds, shuffle enabled, and random_state=42 defined the holdout. This gave 799 training records and 201 test records. Checks confirmed zero shared feature groups, zero shared rows, and complete row coverage.')
table([['Class','Training','Test'],['N',83,20],['P',46,7],['Y',670,174],['Total',799,201]], [180,130,140])
p('Five additional stratified group folds were generated only within the 799 training records and reused for both classifiers. All classes appeared in every training and validation portion. Validation P counts ranged from 4 to 18, explaining some score variability. Macro-F1 was the selection metric because it gives each class equal weight. Accuracy and per-class recall provided complementary views.')
p('The reserved test set was used only after selecting random forest. The selected pipeline was freshly cloned and fitted on all training records, then used to predict test inputs. No model changes were made in response to test results. Earlier whole-dataset summaries were used for the data audit; later EDA and model selection used training data.')

page()
h('5 Classification models and evaluation')
p('A DummyClassifier using the most frequent class served as the baseline. It predicted only Y, giving validation accuracy between 0.796 and 0.873 while P recall remained zero in every fold. N recall is also zero for this behavior. This demonstrates why high accuracy alone is inadequate for the imbalanced task.')
p('Logistic regression used max_iter=2000 and random_state=42 with otherwise default settings. It provides a relatively simple classifier in the transformed feature space. Random forest used 200 trees, random_state=42, and n_jobs=-1. Its trees can capture nonlinear relationships and interactions. No extensive hyperparameter search or class weighting was performed.')
table([['Metric','Logistic regression\nmean (SD)','Random forest\nmean (SD)'],['Accuracy','0.914 (0.033)','0.964 (0.026)'],['Macro-F1','0.658 (0.072)','0.915 (0.069)'],['N recall','0.857 (0.171)','0.942 (0.077)'],['P recall','0.159 (0.106)','0.788 (0.207)'],['Y recall','0.975 (0.014)','0.985 (0.015)']], [140,155,155])
p('These are unweighted means and sample standard deviations over the five validation folds, not confidence intervals. Random forest improved macro-F1 and P recall in every fold. However, its P recall ranged from 0.444 to 1.000, indicating sensitivity to the validation sample. Logistic regression reached high accuracy while often missing most P records.')
page()
h('6 Held out classification results')
table([['Class','Precision','Recall','F1','Support'],['N','0.905','0.950','0.927',20],['P','1.000','1.000','1.000',7],['Y','0.994','0.989','0.991',174],['Macro average','0.966','0.980','0.973',201]], [120,85,80,80,85])
p('The selected random forest correctly classified 198 of 201 test records, giving 98.5% accuracy. The test macro-F1 of 0.973 exceeds the cross-validation mean, but this single split does not establish better expected performance. In particular, perfect P precision and recall apply to only seven test examples; one additional missed P record would change its recall by approximately 14.3 percentage points.')
matrix = Drawing(450,225)
left,bottom,size=115,28,52
matrix.add(String(left+1.5*size,bottom+3*size+37,'Predicted class',fontName='TNR',fontSize=11,textAnchor='middle',fillColor=colors.black))
matrix.add(String(12,bottom+1.5*size,'Actual class',fontName='TNR',fontSize=11,fillColor=colors.black))
for i,label in enumerate(['N','P','Y']):
    matrix.add(String(left+(i+.5)*size,bottom+3*size+12,label,fontName='TNR-Bold',fontSize=11,textAnchor='middle',fillColor=colors.black))
    matrix.add(String(left-15,bottom+(2.5-i)*size-4,label,fontName='TNR-Bold',fontSize=11,textAnchor='middle',fillColor=colors.black))
for row,counts in enumerate([[19,0,1],[0,7,0],[2,0,172]]):
    for col,value in enumerate(counts):
        x=left+col*size;y=bottom+(2-row)*size
        matrix.add(Rect(x,y,size,size,fillColor=None,strokeColor=colors.black,strokeWidth=.6))
        matrix.add(String(x+size/2,y+size/2-4,str(value),fontName='TNR',fontSize=12,textAnchor='middle',fillColor=colors.black))
story.append(matrix)
p('Figure 2  Held out random forest confusion matrix. Rows are actual classes and columns are predictions. The diagonal contains 198 correct predictions; the off diagonal cells contain three errors. Counts total 201 records.')

page()
h('7 Clustering and interpretation')
p('K-means was fitted to training inputs only, after standard scaling and one-hot encoding. It used n_clusters=3, n_init=10, and random_state=42. Three clusters were chosen for an initial comparison with the three supplied classes, not because three natural groups had been established. CLASS was excluded during fitting and used afterward for external evaluation. Cluster numbers have no intrinsic class meaning.')
table([['Cluster','N','P','Y','Total'],[0,2,1,591,594],[1,1,1,9,11],[2,80,44,70,194]], [100,85,85,85,95])
p('Cluster 0 was almost entirely Y. Cluster 2 contained most N and P records but also 70 Y records. Cluster 1 contained only 11 records and mixed all three labels. The clusters therefore did not yield a one-to-one correspondence with the classes.')
table([['Cluster','Median Urea','Median Cr','Median HbA1c','Median BMI'],[0,'4.63','60','9.0','31'],[1,'22.00','401','7.1','33'],[2,'4.45','59','5.4','23']], [65,95,90,110,90])
p('The small cluster had much higher median Urea and Cr than the other clusters. This supports the interpretation that extreme measurements influence the grouping, despite scaling. It does not establish that those records are invalid or identify a clinical condition. Cluster 2 also had a lower median age of 44 compared with 55 and 56 in clusters 0 and 1.')
p('Silhouette was calculated in the same transformed feature space used by K-means and was 0.183, indicating limited separation. Adjusted Rand index (ARI), comparing cluster assignments with known labels while accounting for arbitrary cluster numbering, was 0.572. This shows partial agreement beyond chance rather than perfect recovery. Both scores describe training-data clustering; held-out clustering performance and stability across different K values or seeds were not evaluated.')
h('8 Comparing classification and clustering')
p('Classification learns from labeled examples to predict the supplied target; clustering groups records by similarity without those labels. Random forest is the stronger choice for the stated label-prediction task based on the supervised evaluation. K-means provides a different exploratory view, including a small group with extreme measurements and overlap between N and P. Macro-F1, silhouette, and ARI measure different properties and were calculated in different evaluation settings, so their numeric values cannot be ranked directly against one another.')

page()
h('9 Error analysis')
p('The confusion matrix contains one N record predicted as Y and two Y records predicted as N. All seven P test records were correctly classified. The following table lists selected measurements from the three errors; row index refers to the original spreadsheet row position used by pandas, not a patient identifier.')
table([['Row index','Actual','Predicted','Age','HbA1c','BMI'],[75,'N','Y',59,'4.1','24'],[181,'Y','N',45,'4.0','24'],[216,'Y','N',34,'5.5','21']], [80,65,80,65,80,80])
p('The remaining errors are N-Y confusions. The measurements alone do not establish why the forest made these predictions, and no feature-attribution analysis was performed. Model disagreement was not treated as proof of an incorrect label. Neither records nor labels were changed after inspecting test errors.')
h('10 Limitations and assumptions')
p('Patient identity is the main unresolved evaluation limitation. Feature grouping prevents identical inputs from crossing splits but cannot guarantee that different measurements from one patient stayed together. Scores may therefore overestimate performance on entirely new patients. The test set is small and contains only seven P records. Class imbalance and variable P counts across folds further limit precision of minority-class conclusions.')
p('Units, unusual numeric values, and the process used to create CLASS were not independently verified. HbA1c is both an input and a potentially label-related measurement; whether it contributed to the original labeling process is unknown. Predicting supplied labels is not evidence of prospective disease prediction. Clustering depends on the chosen scaling, feature representation, and K, and may be sensitive to extremes. These results do not establish clinical validity.')
h('11 Future enhancements')
p('First verify patient identifiers, measurement units, and label provenance with the dataset provider, then repeat evaluation using confirmed patient groups and an independent dataset. Investigate flagged values before choosing corrections. Obtain more N and P records to improve evaluation coverage. Compare class weighting and limited hyperparameter tuning using training-only grouped validation. For clustering, assess alternative K values, multiple seeds, robust preprocessing, and alternative algorithms. Assess revisions on new untouched data; do not tune against this test set.')
h('12 Reproducibility and source')
p('Analysis is provided in notebooks/01_diabetes_analysis.ipynb, with package versions in requirements.txt. Use Python 3.10.11, create a virtual environment, install the requirements, place dataset.xlsx in data/raw, and select that environment as the notebook kernel. The notebook locates data from the repository root or its notebooks folder. Restart the kernel and run cells in order. Seeds are fixed at 42 where configured. All computation is local.')
p('Source: Mendeley Data, version 1: https://data.mendeley.com/datasets/wj9rwkp9c2/1. Results are rounded from the accompanying notebook.')

def footer(c, doc):
    c.setFillColor(colors.black)
    c.setFont('TNR', 10)
    if doc.page > 2:
        c.drawCentredString(A4[0]/2, 30, str(doc.page-2))
    elif doc.page == 2:
        c.drawCentredString(A4[0]/2, 30, 'i')

class ReportDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name == 'Heading':
            text=flowable.getPlainText()
            key='section-'+text.split()[0]
            self.canv.bookmarkPage(key)
            self.notify('TOCEntry',(0,text,self.page-2,key))

doc = ReportDoc(str(ROOT/'diabetes_report.pdf'), pagesize=A4,
    rightMargin=60, leftMargin=60, topMargin=45, bottomMargin=47,
    title='Diabetes Classification and Clustering', author='Nihal Mahato')
doc.addPageTemplates(PageTemplate(id='Report',frames=[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id='body')],onPage=footer))
doc.multiBuild(story)
print(ROOT/'diabetes_report.pdf')


