from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoDataSerializer
from .services import OpenAIService

import markdown2
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string

last_conversation_content = {}


class VideoDataView(APIView):
    def post(self, request):
        serializer = VideoDataSerializer(data=request.data)
        if serializer.is_valid():
            assistant_service = OpenAIService()
            try:
                response_data = assistant_service.process_request(
                    serializer.generate_content())
                # Cache content in a dictionary for future PDF export
                if 'data' in response_data and 'value' in response_data['data']:
                    last_conversation_content[assistant_service.thread.id] = response_data['data']['value']
                else:
                    print("Error: 'data' or 'value' not found in response_data")
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Log the exception e
                return Response({"error": "Failed to process request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MusicDataView(APIView):
#     def post(self, request):
#         token = request.headers.get('Authorization', 'default')
#         try:
#             assistant_service = services[token]
#         except KeyError:
#             return Response({'message': 'assistant not found'}, status=status.HTTP_404_NOT_FOUND)
#         try:
#             prompt = "Give me the most appropriate musical style and theme for the script you provided. Use genres and vibes, not specific artists and songs. Please be brief and concise."
#             response_data = assistant_service.process_request(prompt)
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             # Log the exception e
#             return Response({"error": "Failed to process request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GeneratePDFView(APIView):
    def post(self, request):
        id = request.data.get('id', None)
        if id is None:
            return Response({"error": "Missing ID parameter"}, status=status.HTTP_400_BAD_REQUEST)

        if id in last_conversation_content:
            value_content = last_conversation_content[id]
            json_string = {"value": value_content}
        else:
            return Response({"error": "ID not found in conversation content"}, status=status.HTTP_404_NOT_FOUND)

        # 预处理内容
        processed_content = self.preprocess_content(json_string["value"])

        # 将 Markdown 转换为 HTML
        html_content = markdown2.markdown(processed_content, extras=[
                                          "break-on-newline", "tables", "fenced-code-blocks"])

        # 渲染 HTML 模板
        html_string = render_to_string(
            'pdf_template.html', {'content': html_content})

        # 使用 xhtml2pdf 生成 PDF
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(
            html_string, dest=buffer, encoding='UTF-8')

        if pisa_status.err:
            return HttpResponse("PDF generation error: {}".format(pisa_status.err), status=500)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        return response

    def preprocess_content(self, content):
        # 处理换行符
        content = content.replace('\\n', '\n')

        # 移除转义的引号
        content = content.replace('\\"', '"')

        return content
