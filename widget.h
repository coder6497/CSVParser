#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QFileDialog>
#include "dataresult.h"
#include <QPalette>
#include <QBrush>
#include <QColor>
#include <QMessageBox>

QT_BEGIN_NAMESPACE
namespace Ui {
class Widget;
}
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();

private slots:
    void on_pushButton_clicked();
    void on_pushButton_2_clicked();

private:
    Ui::Widget *ui;
    DataResult *dataresult;
signals:
    void show_data(QMap<QString, QString>& text_data);
};
#endif // WIDGET_H
