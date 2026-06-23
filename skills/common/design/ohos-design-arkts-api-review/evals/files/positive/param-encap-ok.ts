// Eval file for rule: 函数入参合理使用参数封装
// 正例1：参数数量不超过5个，无需封装
function connect(host: string, port: number, timeout: number): void {
  // 参数数量为3个，符合规范
}

// 正例2：使用Options模式封装可选参数
interface CreateViewOptions {
  width?: number;
  height?: number;
  backgroundColor?: string;
  borderRadius?: number;
  opacity?: number;
  zIndex?: number;
}

function createView(options: CreateViewOptions): View {
  // 使用Options模式，参数可扩展性强
  return new View(options);
}

// 正例3：使用Builder模式处理复杂参数
class RequestBuilder {
  private url: string = '';
  private method: string = 'GET';
  private headers: Map<string, string> = new Map();
  private body?: string;
  private timeout: number = 30000;
  private retryCount: number = 3;

  setUrl(url: string): RequestBuilder {
    this.url = url;
    return this;
  }

  setMethod(method: string): RequestBuilder {
    this.method = method;
    return this;
  }

  // ... 其他setter方法

  build(): Request {
    return new Request(this);
  }
}

function sendRequest(builder: RequestBuilder): Response {
  // 使用Builder模式，参数设置更灵活
}

// 正例4：将相关参数分组封装
interface Position {
  x: number;
  y: number;
}

interface Size {
  width: number;
  height: number;
}

interface Style {
  color: string;
  fontSize: number;
  fontWeight: string;
}

function drawText(position: Position, size: Size, style: Style, text: string): void {
  // 将相关参数分组封装，参数数量为4个，符合规范
}

// 正例5：使用回调函数参数时，回调不计入参数数量限制
function fetchData(
  url: string,
  method: string,
  headers: Map<string, string>,
  callback: (data: string) => void
): void {
  // 回调函数参数不计入限制，实际参数为3个
}
