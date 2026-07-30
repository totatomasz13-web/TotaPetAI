using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Windows;
using System.Windows.Input;

namespace TotaPetAI;

public partial class MainWindow : Window
{
    private static readonly string PositionFile = Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "TotaPetAI",
        "position.txt");

    public MainWindow()
    {
        InitializeComponent();
    }

    private void Window_Loaded(object sender, RoutedEventArgs e)
    {
        RestorePosition();
    }

    private void Pet_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        if (e.ChangedButton != MouseButton.Left)
        {
            return;
        }

        DragMove();
        KeepOnScreen();
        SavePosition();
    }

    private void DragArea_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
    {
        Pet_MouseLeftButtonDown(sender, e);
    }

    private void ResetPosition_Click(object sender, RoutedEventArgs e)
    {
        SetDefaultPosition();
        SavePosition();
    }

    private void Exit_Click(object sender, RoutedEventArgs e)
    {
        Close();
    }

    private void Window_Closing(object? sender, CancelEventArgs e)
    {
        SavePosition();
    }

    private void RestorePosition()
    {
        try
        {
            if (!File.Exists(PositionFile))
            {
                SetDefaultPosition();
                return;
            }

            string[] values = File.ReadAllText(PositionFile).Split(';');
            if (values.Length != 2 ||
                !double.TryParse(values[0], NumberStyles.Float, CultureInfo.InvariantCulture, out double left) ||
                !double.TryParse(values[1], NumberStyles.Float, CultureInfo.InvariantCulture, out double top))
            {
                SetDefaultPosition();
                return;
            }

            Left = left;
            Top = top;
            KeepOnScreen();
        }
        catch (IOException)
        {
            SetDefaultPosition();
        }
    }

    private void SavePosition()
    {
        try
        {
            Directory.CreateDirectory(Path.GetDirectoryName(PositionFile)!);
            File.WriteAllText(PositionFile, string.Join(";",
                Left.ToString(CultureInfo.InvariantCulture),
                Top.ToString(CultureInfo.InvariantCulture)));
        }
        catch (IOException)
        {
            // Brak zapisu pozycji nie powinien zamykać aplikacji.
        }
    }

    private void SetDefaultPosition()
    {
        Left = SystemParameters.WorkArea.Right - Width - 24;
        Top = SystemParameters.WorkArea.Bottom - Height - 24;
    }

    private void KeepOnScreen()
    {
        Rect area = SystemParameters.WorkArea;
        Left = Math.Clamp(Left, area.Left, area.Right - Width);
        Top = Math.Clamp(Top, area.Top, area.Bottom - Height);
    }
}
