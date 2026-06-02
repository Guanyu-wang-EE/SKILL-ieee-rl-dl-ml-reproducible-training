% monitor_training_template.m
% Lightweight polished monitor for RL/DRL progress.csv files.
% Read CSV only. Do not lock training files. Do not replace final IEEE plotting.

function monitor_training_template(progressCsv, refreshSec, smoothWindow)
if nargin < 1 || isempty(progressCsv)
    progressCsv = 'progress.csv';
end
if nargin < 2 || isempty(refreshSec)
    refreshSec = 5;
end
if nargin < 3 || isempty(smoothWindow)
    smoothWindow = 1;
end

palette = [0.00 0.20 0.40; 0.70 0.13 0.13; 0.00 0.45 0.25; 0.35 0.20 0.55];
fig = figure('Name', 'RL Training Monitor', 'Color', 'w');

while ishandle(fig)
    if ~isfile(progressCsv)
        clf(fig);
        text(0.05, 0.5, ['Waiting for ', progressCsv], 'FontName', 'Times New Roman', 'FontSize', 12);
        drawnow;
        pause(refreshSec);
        continue;
    end

    try
        opts = detectImportOptions(progressCsv);
        tbl = readtable(progressCsv, opts);
    catch err
        clf(fig);
        text(0.05, 0.5, ['CSV read failed: ', err.message], 'FontName', 'Times New Roman', 'FontSize', 11);
        drawnow;
        pause(refreshSec);
        continue;
    end

    if isempty(tbl)
        pause(refreshSec);
        continue;
    end

    [x, xLabel] = chooseX(tbl);
    clf(fig);
    layout = tiledlayout(fig, 2, 2, 'Padding', 'compact', 'TileSpacing', 'compact');
    title(layout, makeTitle(tbl, progressCsv), 'FontName', 'Times New Roman', 'FontSize', 12, 'FontWeight', 'bold');

    plotMetric(tbl, x, xLabel, {'reward'}, 1, 'Reward', palette, smoothWindow);
    plotMetric(tbl, x, xLabel, {'cost', 'violation', 'constraint_violation', 'cv'}, 2, 'Cost / Constraint Violation', palette, smoothWindow);
    plotMetric(tbl, x, xLabel, {'alpha', 'lambda'}, 3, 'Alpha / Lambda', palette, smoothWindow);
    plotMetric(tbl, x, xLabel, {'fps', 'elapsed_sec'}, 4, 'FPS / Elapsed', palette, smoothWindow);

    drawnow;
    pause(refreshSec);
end
end

function [x, xLabel] = chooseX(tbl)
for name = {'step', 'episode'}
    key = name{1};
    if any(strcmp(tbl.Properties.VariableNames, key))
        x = table2array(tbl(:, key));
        xLabel = key;
        return;
    end
end
x = (1:height(tbl))';
xLabel = 'sample';
end

function titleText = makeTitle(tbl, progressCsv)
parts = {progressCsv};
for name = {'env', 'algo', 'seed'}
    key = name{1};
    if any(strcmp(tbl.Properties.VariableNames, key))
        value = tbl{end, key};
        if iscell(value)
            value = value{1};
        end
        parts{end + 1} = [key, '=', char(string(value))]; %#ok<AGROW>
    end
end
titleText = strjoin(parts, ' | ');
end

function plotMetric(tbl, x, xLabel, names, pos, titleText, palette, smoothWindow)
nexttile(pos);
hold on;
found = false;
for i = 1:numel(names)
    name = names{i};
    if any(strcmp(tbl.Properties.VariableNames, name))
        y = table2array(tbl(:, name));
        if smoothWindow > 1 && numel(y) >= smoothWindow
            yPlot = movmean(y, smoothWindow, 'omitnan');
        else
            yPlot = y;
        end
        color = palette(mod(i - 1, size(palette, 1)) + 1, :);
        plot(x, yPlot, 'LineWidth', 1.35, 'Color', color, 'DisplayName', name);
        markAnomalies(x, y, color);
        found = true;
    end
end
if found
    grid on;
    legend('Location', 'best', 'Box', 'off');
else
    text(0.05, 0.5, 'metric not found', 'FontName', 'Times New Roman');
end
xlabel(xLabel, 'FontName', 'Times New Roman');
title(titleText, 'FontName', 'Times New Roman', 'FontSize', 10);
set(gca, 'FontName', 'Times New Roman', 'FontSize', 9, 'LineWidth', 0.8, 'GridAlpha', 0.18);
box on;
hold off;
end

function markAnomalies(x, y, color)
bad = isnan(y) | isinf(y);
if any(bad)
    scatter(x(bad), zeros(sum(bad), 1), 24, color, 'x', 'LineWidth', 1.2, 'DisplayName', 'NaN/Inf');
end
end
