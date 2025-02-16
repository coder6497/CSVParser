#include "widget.h"
#include "ui_widget.h"
#include "script.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
    setWindowTitle("CSVPARSE");
    setFixedSize(600, 400);
    QPalette pal = palette();
    pal.setBrush(QPalette::Window, QBrush(QColor(209, 255, 213), Qt::SolidPattern));
    setPalette(pal);
    QMessageBox msgbox;
    msgbox.setText("ВНИМАНИЕ");
    msgbox.setInformativeText("Данная программа написана криворуким разрабом, который не реализовал обработку ввода неверных данных, поэтому ПОЖАЛУЙСТА ВВОДИТЕ КОРРЕКТНЫЕ ДАННЫЕ ИНАЧЕ У ВАС БУДУТ ПРОБЛЕМЫ");
    msgbox.exec();
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_pushButton_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(nullptr, "Выберите CSV файл", "", "CSV Files (*.csv);;All Files (*)");
    if (!fileName.isEmpty()) {
        ui->label_3->setText(fileName);
    }
}


void Widget::on_pushButton_2_clicked()
{
    QMap<QString, QString> text_data;
    char delimeter = ui->lineEdit->text()[0].toLatin1();
    string key_t = ui->lineEdit_2->text().toStdString(), filename = ui->label_3->text().toStdString();
    vector<vector<string>> data_table = read_file(filename, delimeter);
    map<string, vector<string>> data_map = convert_to_map(data_table);
    map<string, string> data = get_values(data_map, key_t);
    for (auto& [key, value]: data){
        text_data[QString::fromStdString(key)] = QString::fromStdString(value);
    }
    dataresult = new DataResult();
    dataresult->show();
    connect(this, &Widget::show_data, dataresult, &DataResult::updateResultData);
    emit show_data(text_data);
}

