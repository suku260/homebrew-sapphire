class Sapphire < Formula
  desc ""
  homepage "http://www.sapphirelang.info"
  url "http://www.github.com/suku260/Sapphire"
  version "0.5.1"
  sha256 "62411ceb7a6720fbb006bfe0c8e13111e5d0872940439cbc7840d017b9778115"
  
  license "bsd"

  # depends_on "cmake" => :build

  def install
    bin.install "Sapphire"
    # ENV.deparallelize
    system "./configure", "--disable-debug",
                          "--disable-dependency-tracking",
                          "--disable-silent-rules",
                          "--prefix=#{prefix}"
    # system "cmake", ".", *std_cmake_args
    system "make", "install"
  end

  test do
    assert_equal "homebrew", shell_output("#{bin}/sapphire -c 'echo homebrew'").chomp
    system bin/"sapphire", "-c", "printf -v hello -- '%s'"
  end
end
