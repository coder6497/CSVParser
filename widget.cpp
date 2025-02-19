#include "widget.h"
#include "ui_widget.h"
#include "script.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
    setWindowTitle("CSVPARSE");
    setFixedSize(650, 450);
    QPalette pal = palette();
    pal.setBrush(QPalette::Window, QBrush(QColor(209, 255, 213), Qt::SolidPattern));
    setPalette(pal);
    QMessageBox msgbox;
    msgbox.setText("От разработчика");
    msgbox.setInformativeText("Данная программа поддерживает только стандартный формат разделителей CSV(,),"
                              " при попытки обработать файл с другими разделителями вы получите ошибку."
                              " Если фаш файл имеет сторонние разделители, вы можете запустить Python скрипт, который прилагается к данной программе,"
                              " он отредактирует ваш файл под нужный формат разделителей.");
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

void Widget::create_data_result(QMap<QString, QString> text_data){
    if (ui->comboBox->currentIndex() == 1){
        dataresult = new DataResult();
        dataresult->show();
        connect(this, &Widget::show_data, dataresult, &DataResult::updateResultData);
        emit show_data(text_data);
    }
}

void Widget::create_table_show(QList<QStringList> data_table_to_view){
    if (ui->comboBox->currentIndex() == 0){
        tableshow = new TableShow();
        tableshow->show();
        connect(this, &Widget::show_table_data, tableshow, &TableShow::updateTableData);
        emit show_table_data(data_table_to_view);
    }

}

void Widget::on_pushButton_3_clicked()
{
    // Если поля вввода не пустые
    if (!ui->label_3->text().isEmpty() && !ui->lineEdit->text().isEmpty() && !ui->lineEdit_2->text().isEmpty()){

        auto start = chrono::high_resolution_clock::now();
        QMap<QString, QString> text_data;
        char delimeter = ui->lineEdit->text()[0].toLatin1();
        string key_t = ui->lineEdit_2->text().toStdString(), filename = ui->label_3->text().toStdString();

        // Вызов функций обработки данных
        data_table = read_file(filename, delimeter);
        map<string, vector<string>> data_map = convert_to_map(data_table);
        map<string, string> data = get_values(data_map, key_t);
        for (auto& [key, value]: data) text_data[QString::fromStdString(key)] = QString::fromStdString(value);

        QList<QStringList> data_table_to_view;
        for(const auto& row: data_table){
            QStringList temp_lst;
            for(const auto& elem: row){
                temp_lst.append(QString::fromStdString(elem));
            }
            data_table_to_view.append(temp_lst);
        }
        create_data_result(text_data);
        create_table_show(data_table_to_view);
    }
}



