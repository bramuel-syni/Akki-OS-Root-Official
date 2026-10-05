"""Bounded structural validation only, not malware scanning or audio quality analysis."""
import csv
import io
import json
import os
import re
import unicodedata
from pathlib import PurePath

FORMATS={
 '.wav':('audio','audio/wav'),'.mp3':('audio','audio/mpeg'),'.flac':('audio','audio/flac'),
 '.ogg':('audio','audio/ogg'),'.m4a':('audio','audio/mp4'),
 '.txt':('transcript','text/plain'),'.vtt':('transcript','text/vtt'),'.srt':('transcript','text/plain'),
 '.json':('labels','application/json'),'.csv':('labels','text/csv'),
 '.xlsx':('labels','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}


def describe(filename,size):
    filename=unicodedata.normalize('NFKC',filename)
    if any(ord(c)<32 for c in filename) or '/' in filename or '\\' in filename:
        raise ValueError('Use a file name, not a path')
    ext=PurePath(filename).suffix.lower()
    if ext not in FORMATS: raise ValueError('Unsupported format. Choose audio, a transcript or a JSON/CSV label file.')
    kind,mime=FORMATS[ext]
    limit=int(os.environ['MEDIA_MAX_FILE_BYTES' if kind=='audio' else 'MEDIA_MAX_TEXT_BYTES'])
    if size>limit: raise ValueError(f'This file exceeds the {limit/1000000:g} MB limit')
    stem=PurePath(filename).stem
    title=re.sub(r'[_]+',' ',stem).strip()
    if re.fullmatch(r'[a-fA-F0-9-]{12,}',title): title={'audio':'Audio recording','transcript':'Transcript','labels':'Label manifest'}[kind]
    return {'filename':filename,'extension':ext,'kind':kind,'content_type':mime,'title':title[:140] or 'Untitled file'}


def validate(file,ext):
    file.seek(0); prefix=file.read(64); file.seek(0)
    signatures={'.wav':lambda:prefix[:4] in (b'RIFF',b'RF64') and prefix[8:12]==b'WAVE',
                '.mp3':lambda:prefix[:3]==b'ID3' or (len(prefix)>1 and prefix[0]==255 and prefix[1]&224==224),
                '.flac':lambda:prefix[:4]==b'fLaC','.ogg':lambda:prefix[:4]==b'OggS',
                '.m4a':lambda:prefix[4:8]==b'ftyp'}
    if ext in signatures:
        if not signatures[ext](): raise ValueError('File contents do not match the selected audio format')
        return {'check':'container_signature_only','audio_quality':'not_measured','duration_seconds':None,'malware_scan':'not_performed'}
    if ext=='.xlsx':
        if prefix[:4]!=b'PK\x03\x04': raise ValueError('File contents are not an XLSX workbook')
        import openpyxl
        try:
            book=openpyxl.load_workbook(file,read_only=True,data_only=True)
            sheets=len(book.worksheets); rows=sum(1 for ws in book.worksheets for _ in ws.iter_rows(min_row=2,values_only=True))
        except Exception: raise ValueError('Invalid XLSX workbook')
        finally: file.seek(0)
        if rows<1: raise ValueError('An XLSX workbook needs a header and at least one data row')
        return {'check':'xlsx_structure','sheets':sheets,'rows':rows,'label_taxonomy':'not_verified','malware_scan':'not_performed'}
    try: text=file.read().decode('utf-8-sig')
    except UnicodeError: raise ValueError('Text and label files must use UTF-8 encoding')
    finally: file.seek(0)
    if '\x00' in text: raise ValueError('Binary contents are not a text file')
    if not text.strip(): raise ValueError('The text file is empty')
    result={'check':'utf8_text','malware_scan':'not_performed'}
    if ext=='.json':
        try: data=json.loads(text)
        except (ValueError,RecursionError): raise ValueError('Invalid JSON label file')
        if not isinstance(data,(dict,list)): raise ValueError('A label manifest must be a JSON object or array')
        result.update(check='json_syntax',label_taxonomy='not_verified')
    if ext=='.csv':
        try:
            reader=csv.reader(io.StringIO(text),strict=True)
            header=next(reader)
            rows=0
            for row in reader:
                if len(row)!=len(header): raise ValueError('CSV rows must match the header columns')
                rows+=1
            if len(header)<2 or rows<1: raise ValueError('A CSV label file needs a header and at least one data row')
        except (csv.Error,StopIteration): raise ValueError('Invalid CSV label file')
        result.update(check='csv_syntax',rows=rows,label_taxonomy='not_verified')
    return result