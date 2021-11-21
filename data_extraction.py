import scispacy
import spacy
import pandas as pd
import io
import os
# Core models
# import en_core_sci_sm
import en_core_sci_lg

# NER specific models
import en_ner_craft_md
import en_ner_bc5cdr_md
import en_ner_jnlpba_md
import en_ner_bionlp13cg_md


# install models for NLP and NER using Scispacy
# pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_craft_md-0.4.0.tar.gz
# pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_jnlpba_md-0.4.0.tar.gz
# pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bc5cdr_md-0.4.0.tar.gz
# pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bionlp13cg_md-0.4.0.tar.gz
# pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_lg-0.4.0.tar.gz

# import data

class DataExtraction:

    def run(file):

        df = pd.read_csv(rf"pubmed\{file}")

        # Pick specific Abstract to use (row 0, column "Abstract")
        text = df.loc[0, "Abstract"]

        # Load specific model and pass text through
        nlp = en_core_sci_lg.load()
        doc = nlp(text)

        # Display resulting entity extraction
        # displacy_image = displacy.render(doc, jupyter=True,style='ent')

        # Load the models
        nlp_cr = en_ner_craft_md.load()
        nlp_bc = en_ner_bc5cdr_md.load()
        nlp_bi = en_ner_bionlp13cg_md.load()
        nlp_jn = en_ner_jnlpba_md.load()

        # Methods to add entity/value pairs to table¶
        def add_cr(AbstractList, doiList):
            i = 0
            table = {"doi": [], "Entity": [], "Class": []}
            for doc in nlp_cr.pipe(AbstractList):
                doi = doiList[i]
                for x in doc.ents:
                    table["doi"].append(doi)
                    table["Entity"].append(x.text)
                    table["Class"].append(x.label_)
                i += 1
            return table

        def add_bc(AbstractList, doiList):
            i = 0
            table = {"doi": [], "Entity": [], "Class": []}
            for doc in nlp_bc.pipe(AbstractList):
                doi = doiList[i]
                for x in doc.ents:
                    table["doi"].append(doi)
                    table["Entity"].append(x.text)
                    table["Class"].append(x.label_)
                i += 1
            return table

        def add_jn(AbstractList, doiList):
            i = 0
            table = {"doi": [], "Entity": [], "Class": []}
            for doc in nlp_jn.pipe(AbstractList):
                doi = doiList[i]
                for x in doc.ents:
                    table["doi"].append(doi)
                    table["Entity"].append(x.text)
                    table["Class"].append(x.label_)
                i += 1
            return table

        def add_bi(AbstractList, doiList):
            i = 0
            table = {"doi": [], "Entity": [], "Class": []}
            for doc in nlp_bi.pipe(AbstractList):
                doi = doiList[i]
                for x in doc.ents:
                    table["doi"].append(doi)
                    table["Entity"].append(x.text)
                    table["Class"].append(x.label_)
                i += 1
            return table

        # Read in Entire File (Main Function)¶
        #Read in file
        df = pd.read_csv(rf"pubmed\{file}")

        # Sort out blank Abstracts
        df = df.dropna(subset=['Abstract'])

        # Create lists
        doiList = df['doi'].tolist()
        AbstractList = df['Abstract'].tolist()

        file = file.split('.csv')

        file = file[0] + file[1] + '.csv'

        # 1_Next Model_Entity Types_(GGP, SO, TAXON, CHEBI, GO, CL)
        # Add all entity value pairs to table (run one at a time, each ones takes ~20 min)
        table = add_cr(AbstractList, doiList)

        # Turn table into an exportable CSV file (returns normalized file of entity/value pairs)
        trans_df = pd.DataFrame(table)
        trans_df.to_csv(
            rf"pubmed_text_mining\{file}_Breast_Entity_pairings.csv", index=False)

        # 2_Next Model_Entity Types (DISEASE, CHEMICAL)
        # Add all entity value pairs to table (run one at a time, each ones takes ~20 min)
        table = add_bc(AbstractList, doiList)

        # Turn table into an exportable CSV file (returns normalized file of entity/value pairs)
        trans_df = pd.DataFrame(table)
        trans_df.to_csv(
            rf"pubmed_text_mining\{file}_DISEASE_CHEMICAL_Entity_pairings.csv", index=False)

        # 3_Next Model_Entity Types_(AMINO_ACID, ANATOMICAL_SYSTEM, CANCER, CELL, CELLULAR_COMPONENT, DEVELOPING_ANATOMICAL_STRUCTURE, GENE_OR_GENE_PRODUCT, IMMATERIAL_ANATOMICAL_ENTITY, MULTI-TISSUE_STRUCTURE, ORGAN, ORGANISM, ORGANISM_SUBDIVISION, ORGANISM_SUBSTANCE, PATHOLOGICAL_FORMATION, SIMPLE_CHEMICAL, TISSUE)
        # Add all entity value pairs to table (run one at a time, each ones takes ~20 min)
        table = add_bi(AbstractList, doiList)

        # Turn table into an exportable CSV file (returns normalized file of entity/value pairs)
        trans_df = pd.DataFrame(table)
        trans_df.to_csv(
            rf"pubmed_text_mining\{file}_bionlp_Entity_pairings.csv", index=False)

        # 4_Next Model_Entity Types_(DNA, CELL_TYPE, CELL_LINE, RNA, PROTEIN)
        # Add all entity value pairs to table (run one at a time, each ones takes ~20 min)
        table = add_jn(AbstractList, doiList)

        # Turn table into an exportable CSV file (returns normalized file of entity/value pairs)
        trans_df = pd.DataFrame(table)
        trans_df.to_csv(
            rf"pubmed_text_mining\{file}_DNA_CELL_TYPE_CELL_LINE_RNA_PROTEIN_Entity_pairings.csv", index=False)
