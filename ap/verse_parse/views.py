from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.core.context_processors import csrf
from django.template import RequestContext, Context,loader

from verse_parse.forms import UploadFileForm, DisplayForm

#imports for pdfminer
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from cStringIO import StringIO
import re

from verse_parse import outline, references

def handle_uploaded_file(f):
	'''
	Takes uploaded pdf file, returns outline of verse references.
	Gets verse text from references.
	Basically gets all needed data for HTML template.
	'''
	data = pdf_to_text(f)
	partition = data.partition('Scripture Reading:')
	title = outline.get_title(partition[0])
	ref_outline = outline.extract_references(partition[2])

	for i in range(len(ref_outline)):
		outline_pt = ref_outline[i]

		for ref in outline_pt['refs']:				
			ref['string'] = references.reference_to_string(ref)

			if ref['chapter'] is not None:
				ref['repeat'] = outline.find_repeat(ref_outline, ref, i)


				if ref['repeat'] == False:
					ref['verses'] = references.get_verses(ref)
	return (title, ref_outline)

def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)

		if form.is_valid():
			(title, ref_outline)=handle_uploaded_file(request.FILES['file'])
			
			display_template = loader.get_template('verse_parse/verse_sheet.html')
			context = Context({'outline': ref_outline,
							   'title': title,})
			return HttpResponse(display_template.render(context))
			
		else:
			#return HttpResponse("Form invalid")
			c = {'form': form}
			c.update(csrf(request))
	
			return render_to_response('verse_parse/upload.html', c)
	else:
		form = UploadFileForm()
	
	c = {'form': form}
	c.update(csrf(request))
	
	return render_to_response('verse_parse/upload.html', c)


def pdf_to_text(fname):
    
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    codec = 'utf-8'
    caching = True
    showpageno = True
    laparams = LAParams()
    
   
    rsrcmgr = PDFResourceManager(caching=caching)
    outfp = StringIO()
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fname, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            interpreter.process_page(page)
    device.close()
    return outfp.getvalue()
