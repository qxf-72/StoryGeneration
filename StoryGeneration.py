import sys
from openai import OpenAI
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtGui import QFont

class StoryGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('智能写作辅助工具')
        
        # 设置窗口的初始大小
        self.resize(1500, 1000)  

        # 设置字体
        font = QFont()
        font.setPointSize(12)  # 设置字体大小为12

        # 创建控件
        self.theme_input = QTextEdit(self)
        self.theme_input.setPlaceholderText("请输入主题")
        self.theme_input.setFont(font)

        self.character_input = QTextEdit(self)
        self.character_input.setPlaceholderText("请输入角色性格")
        self.character_input.setFont(font)

        self.setting_input = QTextEdit(self)
        self.setting_input.setPlaceholderText("请输入设定")
        self.setting_input.setFont(font)

        self.additional_input = QTextEdit(self)
        self.additional_input.setPlaceholderText("请输入其他补充信息")
        self.additional_input.setFont(font)

        self.generate_button = QPushButton('生成故事', self)
        self.generate_button.setFont(font)
        self.generate_button.clicked.connect(self.generate_story)

        self.adjust_button = QPushButton('调整大纲', self)
        self.adjust_button.setFont(font)
        self.adjust_button.clicked.connect(self.adjust_outline)

        self.story_output = QTextEdit(self)
        self.story_output.setPlaceholderText("故事大纲将在这里显示...")
        self.story_output.setReadOnly(True)
        self.story_output.setFont(font)

        # 设置 QLabel 的字体
        label_font = QFont()
        label_font.setPointSize(12)  # 设置 QLabel 字体大小
        self.theme_label = QLabel("主题")
        self.theme_label.setFont(label_font)
        
        self.character_label = QLabel("角色性格")
        self.character_label.setFont(label_font)

        self.setting_label = QLabel("设定")
        self.setting_label.setFont(label_font)

        self.additional_label = QLabel("其他补充信息")
        self.additional_label.setFont(label_font)

        # 初始化对话历史
        self.history = [
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
        ]
        
        # 左边布局（输入框和按钮）
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.theme_label)
        left_layout.addWidget(self.theme_input)
        left_layout.addWidget(self.character_label)
        left_layout.addWidget(self.character_input)
        left_layout.addWidget(self.setting_label)
        left_layout.addWidget(self.setting_input)
        left_layout.addWidget(self.additional_label)
        left_layout.addWidget(self.additional_input)
        left_layout.addWidget(self.generate_button)
        left_layout.addWidget(self.adjust_button)

        # 右边布局（显示生成的故事）
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.story_output)

        # 主布局，左右布局并排
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)  # 左边占1部分
        main_layout.addLayout(right_layout, 2)  # 右边占2部分

        # 设置窗口的主布局
        self.setLayout(main_layout)

    def generate_story(self):
        # 获取用户输入
        theme = self.theme_input.toPlainText()
        character = self.character_input.toPlainText()
        setting = self.setting_input.toPlainText()
        additional = self.additional_input.toPlainText()

        # 将新的对话添加到历史记录
        self.history.append({
            "role": "user", 
            "content": f"主题：{theme}\n角色性格：{character}\n设定：{setting}\n其他补充信息：{additional}"
        })

        # 创建 OpenAI 客户端，进行 API 调用
        client = OpenAI(
            api_key="sk-7HoO7fEXZ9JAVnhFwDA9VBgcnKGKBdxz8L7Q5PaLmQtHXvzL",  
            base_url="https://api.moonshot.cn/v1",
        )
        
        # 调用生成故事的接口
        try:
            completion = client.chat.completions.create(
                model="moonshot-v1-8k", 
                messages=self.history,
                temperature=0.3,
            )
            # 从响应中提取生成的故事内容
            story = completion.choices[0].message.content
            self.story_output.setText(story)

            # 将生成的故事添加到对话历史
            self.history.append({
                "role": "assistant",
                "content": story
            })
        except Exception as e:
            self.story_output.setText(f"请求失败: {e}")

    def adjust_outline(self):
        # 创建弹出窗口
        dialog = QDialog(self)
        dialog.setWindowTitle("调整大纲")
        
        layout = QVBoxLayout()
        
        # 创建文本框用于输入调整内容
        self.adjust_input = QTextEdit(dialog)
        self.adjust_input.setPlaceholderText("请输入调整内容")
        layout.addWidget(self.adjust_input)

        # 创建按钮组
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        button_box.accepted.connect(self.apply_adjustment)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def apply_adjustment(self):
        # 获取调整的内容
        adjustment = self.adjust_input.toPlainText()

        # 将调整内容添加到对话历史
        self.history.append({
            "role": "user", 
            "content": f"请根据以下调整改进故事大纲：{adjustment}"
        })

        # 创建 OpenAI 客户端，进行 API 调用
        client = OpenAI(
            api_key="sk-7HoO7fEXZ9JAVnhFwDA9VBgcnKGKBdxz8L7Q5PaLmQtHXvzL", 
            base_url="https://api.moonshot.cn/v1",
        )
        
        # 调用生成改进后的故事大纲
        try:
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",  # 使用你所需要的模型
                messages=self.history,
                temperature=0.3,
            )
            # 从响应中提取改进后的故事内容
            updated_story = completion.choices[0].message.content
            self.story_output.setText(updated_story)

            # 将改进后的故事添加到对话历史
            self.history.append({
                "role": "assistant",
                "content": updated_story
            })
        except Exception as e:
            self.story_output.setText(f"请求失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StoryGeneratorApp()
    window.show()
    sys.exit(app.exec_())
